"""
This script can be used for analyzing paired ram interactions with a specific game-object property. This is an extension of
considering only the correlation of the property with each ram position individually (as in "find_correlation.py").
To reduce the number of RAM pairs for which to test for interactions, two measures are taken:
First, a statistic over the correlation values of all ram positions is computed. The threshhold correlation above which
to pick the test pairs can be specified as a quantile ("-q") argument. Secondly, during data acquisition, a set of observed
values for each ram position is saved, so not all 256x256 theoretically possible value-pairs have to be tested.
In the analysis run, all ram pairs are tested for influence on the specified property by probing every combination of their ram-value
sets. The found property values and responsible ram pairs (denoted by ram number and value) are sorted by ascending property value and
displayed in a 2D scatter-plot. Property values from the data acquisition phase are compared to those generated during the probing phase,
in terms of number of unique values, range and step size. This acts as a simple check that the found interactions match the expected
behaviour. During the probing phase, the observations (game images) are also checked for invalid game-crash-like interactions, in which case
the proposed value pair is discarded. The mappings from property value to ram pairs can be summarized and exported as a csv-file.

Currently, the analysis can only take one game object and one property only. Generally though, it could be extended to multiple targets.
It is recommended to provide a snapshot where the desired object is already present.
"""

# TODO: No unique mapping, yet, for most values -> Further filtering and validationof ram pairs required.

# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
from copy import deepcopy
from tqdm import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import RANSACRegressor, LinearRegression
from os import path
import pathlib
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))  # noqa
from ocatari.core import OCAtari
from ocatari.utils import parser, load_agent, make_deterministic
import pickle
from time import sleep


parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-to", "--tracked_objects", type=str, default=["Player"], nargs='+',
                    help="A list of objects to track")
parser.add_argument("-tp", "--tracked_properties", type=str, default=['x', 'y'], nargs='+',
                    help="A list of properties to track for each object")
parser.add_argument("-ns", "--nb_samples", type=int, default=1000,
                    help="The number of samples to use.")
parser.add_argument("-dqn", "--dqn", action="store_true", help="Use DQN agent")
parser.add_argument("-s", "--seed", default=0,
                    help="Seed to make everything deterministic")
parser.add_argument("-r", "--render", action="store_true",
                    help="If provided, renders")
parser.add_argument("-m", "--method", type=str, default="pearson", choices={"pearson", "spearman", "kendall"},
                    help="The method to use for computing the correlation")
parser.add_argument("-snap", "--snapshot", type=str, default=None,
                    help="Path to an emulator state snapshot to start from.")
parser.add_argument("-q", "--quantile", type=float,
                    help="The quantile for filtering RAM pairs based on correlation value")

opts = parser.parse_args()

# headroom in percent for number of pixel changes between consecutive images
diff_headroom = 0.1

MODE = "vision"
if opts.render:
    RENDER_MODE = "human"
else:
    RENDER_MODE = "rgb_array"
env = OCAtari(opts.game, mode=MODE, render_mode=RENDER_MODE)

make_deterministic(opts.seed, env)

observation, info = env.reset()
if opts.snapshot:
    snapshot = pickle.load(open(opts.snapshot, "rb"))
    env._env.env.env.ale.restoreState(snapshot)


def viz_correlations(corr, n_bins='auto'):
    """Visualizes the correlation matrix of all ram states and a histogram over pairwise correlation values. The diagonal ones of the
    correlation matrix are ignored for the histogram."""

    corr = corr.to_numpy()
    diag_mask = np.eye(corr.shape[0])  # mask out the diagonal
    corr[diag_mask == 1] = np.nan
    corr_values = np.ravel(corr)
    corr_values = corr_values[~np.isnan(corr_values)]

    fig, axs = plt.subplots(1, 2)
    img = axs[0].matshow(corr)
    plt.colorbar(mappable=img, orientation='vertical', label='correlation')
    axs[0].set_title('Correlation Matrix of RAM Positions')
    axs[1].hist(corr_values, n_bins, density=True)
    axs[1].set_title(
        'Histogram over correlation values (corrected for diagonal ones)')
    plt.show()


def find_corr_pairs(corr, quantile):
    """Reduce the set of test ram-pairs by selecting those above a specified correlation threshold (given as a quantile). """

    top_perc = np.round((1 - quantile)*100)
    print(f"\nFiltering RAM Pairs with top {top_perc} % correlation...\n")
    high_corrs = list()     # list of tuples for candidate ram-pairs
    positions = list()      # list of ram positions included in the candidate pairs

    # Mask out duplicate lower triangle of correlation matrix
    corr_upper_tri = corr.mask(np.tril(np.ones(corr.shape)).astype(bool))
    masked_array = corr_upper_tri.to_numpy()
    # Compute the threshold (quantile) value
    thresh = np.nanquantile(masked_array, opts.quantile)
    thresh_mask = corr_upper_tri.where((corr_upper_tri.abs() > thresh) & (
        corr_upper_tri.abs() < 1))  # mask out all values below quantile

    for index, row in thresh_mask.iterrows():   # iterate over rows of mask matrix to generate ram-pair candidates

        if row.isna().all(axis=None):
            continue
        # positions := first element of ram pair
        positions.append(index)
        # labels := second element(s) of ram pair
        labels = row.dropna().index.tolist()
        positions.extend(labels)
        ram_pairs = [(int(index), int(label))
                     for label in labels]      # crate tuple of ram positions
        high_corrs.extend(ram_pairs)
        print(f"{index} -> {labels}")

    # set of ram positions that are included in the found pairs
    positions = np.unique(np.array(positions, dtype=int))
    print(
        f"\nFound {len(high_corrs)} RAM pairs above the specified correlation threshold (ones excluded)")
    # plot the masked and thresholded correlation matrix
    fig, ax = plt.subplots()
    img = ax.matshow(thresh_mask)
    plt.colorbar(mappable=img, orientation='vertical', label='correlation')
    ax.set_title(f"Top {top_perc} % correlated RAM Positions (ones excluded)")
    plt.show()

    return high_corrs, positions


def compare_prop_stats(observed, generated):
    """ Used to check, whether the found interactions are close to the ground-truth actions.
    Compares a few simple statistics of the tracked property from the acquisition run (random/agent-based gameplay) and
    the generated property values from the analysis run (probing ram pairs and ram values).
    Compared are the number of unique values, the range of values and the step size."""

    target = f"{opts.tracked_objects[0]} - {opts.tracked_properties[0]}"
    source_lines = ('Observed', 'Generated')

    for prop_saves, header_prefix in zip((observed, generated), source_lines):
        prop_saves = np.array(prop_saves)
        unique_prop_vals = np.unique(prop_saves)
        prop_bounds = tuple([min(prop_saves), max(prop_saves)])
        if header_prefix == 'Generated':
            d_prop = np.abs(np.diff(unique_prop_vals))
        else:
            d_prop = np.abs(np.diff(prop_saves))
        uniques, indices, counts = np.unique(
            d_prop, return_index=True, return_counts=True)
        prop_step_size = uniques[np.argmax(counts)]
        print('-------------')
        print(f"{header_prefix} stats for {target}:\n")
        print(
            f"Number of unique values: {unique_prop_vals.size}\nRange: {prop_bounds}\n Main Step Size: {prop_step_size}\n")

    return


class InteractionCandidate:
    """Helper class used to represent ram-pair candidates.

    Attributes
    ----------
    ram_pair : tuple
        The ram positions of the pair.
    ram_values : list of tuples.
        The paired values of the ram positions for which a valid interaction was found.
    prop_values : list
        The property values corresponding to each pair of ram values.

    Methods
    -------
    get_ram_pair()
        Returns the tuple of ram positions.
    get_ram_values()
        Splits the ram-value tuples into seperate numpy arrays for each ram position and returns the arrays.
    get_prop_values()
        Returns a numpy array of the pair's property values.

    """

    def __init__(self, ram_pair, ram_values, prop_values):

        self.ram_pair = ram_pair
        self.ram_values = ram_values
        self.prop_values = prop_values

    def get_ram_pair(self):
        return self.ram_pair

    def get_ram_values(self):
        ram1vals, ram2vals = tuple(zip(*self.ram_values))
        ram1vals = np.array(list(ram1vals))
        ram2vals = np.array(list(ram2vals))

        return ram1vals, ram2vals

    def get_prop_values(self):
        prop_vals = np.array(self.prop_values)

        return prop_vals


class InteractionTracker:
    """This class contains the analysis process for searching for ram-pair--property interactions.

    Attributes
    ----------
    env : obj
        OC Atari environment.
    anchor_state : obj
        State of the OC Atari environment used as a base for observations.
    base_obs : numpy array
        Three-channel RGB image from the base state of the environment.
    positions : numpy array
        Set of ram positions included in the test-pairs.
    ram_data : Pandas DataFrame
        Data frame of ram states from the acquisition run.
    high_corrs : list of tuples
        The ram-pair candidates to test.
    cat : str
        Category of the tracked game object.
    prop : str
        The tracked property.
    test_values : dict
        Mapping of (ram position -> set of ram values to test)
    interactions : list
        The found interactions as instances of the InteractionCandidate class.
    old_prop : float
        The base property value to compare against.

    Methods
    -------
    show_obs(obs)
        Plot a rendering of the environment (here, the base-state rendering).
    test_all_ram_pairs(diff_ceil)
        Run the analysis on all candidate ram pairs and ram values.
    plot_interaction_summary()
        Creates a plot summarizing all found interactions.
        Ram-pairs and respective values (x) -> Generated roperty value (y)
    create_interaction_report()
        Creates a Pandas DataFrame from the found interactions and saves it as a
        .csv file to a user-specified location.

    """

    def __init__(self, env, obj_cat, property, ram_data, high_corrs, positions):

        if opts.snapshot:
            self.anchor_state = pickle.load(open(opts.snapshot, "rb"))
        else:
            self.anchor_state = env._clone_state()

        self.env = env
        self._restore_env()
        self.base_obs, _, _, _, _ = self.env.step(0)
        self.show_obs(self.base_obs)
        self.positions = positions
        self.ram_data = ram_data
        self.high_corrs = high_corrs
        self.cat = obj_cat
        self.prop = property
        self.test_values = dict()
        self.interactions = list()
        self._generate_test_values()
        self.old_prop = self._fetch_base_prop_value()

    def show_obs(self, obs):
        fig, ax = plt.subplots()
        im = ax.imshow(obs)
        ax.set_title("Base Observation")
        plt.show()

        return

    def _fetch_base_prop_value(self):
        """Gets the base property value for the tracked object from the base env state."""

        for obj in env.objects:
            if self.cat == obj.category:
                prop_value = obj.__getattribute__(self.prop)
                print(
                    f"Base value of {opts.tracked_objects[0]}-{opts.tracked_properties[0]}: {prop_value}")
                return prop_value
            else:
                continue

    def _generate_test_values(self):
        """Empirically generates a set of ram values for each ram position included in the test-candidates."""

        print('\nGenerating test-value sets for RAM positions...\n')

        for ram_pos in self.positions:
            values = self.ram_data.loc[:, str(ram_pos)].unique()
            self.test_values[ram_pos] = values
            # print(f"RAM {ram_pos} ({values.size} values)")

    def _restore_env(self):
        observation, info, self.env.reset()
        self.env._env.env.env.ale.restoreState(self.anchor_state)
        return

    def _check_property_change(self):
        """Checks, whether a pairwise ram manipulation caused a valid property change.
        Returns the new property value, or NaN for invalids. The img difference ceiling is computed after the acquisition run.
        """

        update_prop = np.nan
        obs, reward, terminated, truncated, info = self.env.step(0)
        nb_diff = np.sum(obs != self.base_obs) // 3
        if nb_diff > self.diff_ceil:
            update_prop = np.nan
        else:
            current_objects = dict([(obj.category, obj)
                                   for obj in env.objects])
            if self.cat in current_objects.keys():
                new_prop = current_objects[self.cat].__getattribute__(
                    self.prop)
                if (new_prop - self.old_prop) != 0:
                    update_prop = new_prop
                else:
                    update_prop = np.nan

        if terminated or truncated:
            self._restore_env()

        return update_prop

    def _test_interactions(self, test_pair):
        """Main method for iterating through ram value combinations for a ram pair."""

        from itertools import compress

        pos1, pos2 = test_pair
        prop_vals = list()
        ram_vals = list()

        for val1 in self.test_values[pos1]:
            for val2 in self.test_values[pos2]:
                self._restore_env()
                self.env.unwrapped.ale.setRAM(pos1, val1)
                self.env.unwrapped.ale.setRAM(pos2, val2)
                new_prop_val = self._check_property_change()
                ram_vals.append((val1, val2))
                prop_vals.append(new_prop_val)

        prop_vals = np.array(prop_vals)
        to_keep = ~np.isnan(prop_vals)
        ram_vals_tokeep = list(compress(ram_vals, to_keep.tolist()))
        # print(f"\nInteractions found for pair {test_pair}: {np.count_nonzero(to_keep)}")
        # print(f"RAM Vals to keep: {ram_vals_tokeep}")
        # print(f"Proposed values to keep: {prop_vals[to_keep]}")
        kept_vals = np.count_nonzero(to_keep)

        if (kept_vals > 10):
            icandit = InteractionCandidate(
                ram_pair=test_pair, ram_values=ram_vals_tokeep, prop_values=prop_vals[to_keep])
            self.interactions.append(icandit)
        else:
            pass

        return

    def test_all_ram_pairs(self, diff_ceil):
        """Method to call for a full analysis run. Returns the found interactions.

        Parameters
        ----------
        diff_ceil : int
            When checking for invalid interactions (e.g. game-crashes, image disruptions) the number of pixel differences
            is compared to this value.

        """

        self.diff_ceil = diff_ceil

        print("\nTesting proposed RAM pairs for interactions...\n")
        with tqdm(self.high_corrs) as pbar:
            for ram_pair in pbar:
                pbar.set_description(f"{ram_pair[0]} and {ram_pair[1]}")
                self._test_interactions(ram_pair)
        print(f"Found {len(self.interactions)} candidate interaction pairs.\n")

        return self.interactions

    def plot_interactions_single(self):
        """Method for creating 3D plots of (RAM 1 value (x), RAM 2 value (y)) -> (Property Value (z)) for each ram pair."""
        for candidate in self.interactions:
            ram1, ram2 = candidate.get_ram_pair()
            ram1vals, ram2vals = candidate.get_ram_values()
            prop_vals = candidate.get_prop_values()

            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            ax.scatter(ram1vals, ram2vals, prop_vals)

            ax.set_xlabel(f"RAM {ram1} value")
            ax.set_ylabel(f"RAM {ram2} value")
            ax.set_zlabel(
                f"{opts.tracked_objects[0]} {opts.tracked_properties[0]}")
            ax.set_title(
                f"Interactions of  {opts.tracked_objects[0]} {opts.tracked_properties[0]} with ram pair {(ram1, ram2)}")
            plt.show()

        return

    def _merge_data(self):
        """Summarizes the data from all interaction candidates into seperate arrays and generates the x-axis labels for the
        data points.
        """

        y = list()
        xlabels = list()

        for candidate in self.interactions:
            prop_vals = candidate.get_prop_values()
            y.extend(prop_vals)
            val1labels, val2labels = candidate.get_ram_values()
            ram_label = candidate.get_ram_pair()
            for i in range(prop_vals.size):
                label = f"R{ram_label[0]}:{val1labels[i]}| R{ram_label[1]}:{val2labels[i]}"
                xlabels.append(label)
        y = np.array(y)
        xlabels = np.array(xlabels)
        uniques, unique_indices, unique_counts = np.unique(
            y, return_index=True, return_counts=True)

        return y, xlabels, uniques, unique_indices, unique_counts

    def plot_interaction_summary(self):
        """Plots all found valid interactions (RAM positions & Values) -> (Property value)."""

        print("\nCreating summary plot. This may take a while...\n")
        y, xlabels, uniques, unique_indices, unique_counts = self._merge_data()

        sort_indices = np.argsort(y)
        y_sorted = y[sort_indices]
        labels_sorted = xlabels[sort_indices]

        unique_y = uniques[unique_counts == 1]
        unique_indices = unique_indices[unique_counts == 1]
        unique_labels = xlabels[unique_indices]
        print(
            f"Found {uniques.size} unique values for {opts.tracked_properties[0]}")
        print(
            f"Values for {opts.tracked_properties[0]} with unique mapping: {unique_y.size}")

        x = np.arange(xlabels.size)

        obj_and_prop = f"{opts.tracked_objects[0]} {opts.tracked_properties[0]}"

        fig, ax = plt.subplots()
        ax.scatter(x, y_sorted)
        ax.set_xticks(ticks=x, labels=labels_sorted,
                      rotation=-90, fontsize='xx-small')
        ax.set_xlabel("RAM pairs and respective values")
        ax.set_ylabel(obj_and_prop)
        ax.set_title(
            f"Summarized pairwise RAM interactions for {obj_and_prop}")
        plt.subplots_adjust(bottom=0.15)

        plt.show()

    def create_interaction_report(self):
        """Creates a Pandas DataFrame from the found interactions and saves it to a specified location.

        Details
        -------
        Rows: RAM pair (positions & values)
        Columns : sorted property values
        Export format: csv

        The table is padded with NaN to the maximum number of rows.
        """

        obj_and_prop = f"{opts.tracked_objects[0]} {opts.tracked_properties[0]}"

        y, xlabels, uniques, unique_indices, unique_counts = self._merge_data()
        report = dict()
        sort_indices = np.argsort(y)
        xlabels_sort = xlabels[sort_indices]
        max_len = np.max(unique_counts)

        report_header = f"\nOverview of mappings found for values of {obj_and_prop}"
        sep_long = "========================="

        start_idx = 0

        for val in uniques:
            end_idx = start_idx + unique_counts[uniques == val][0]
            labels_to_add = xlabels_sort[start_idx:end_idx]
            padded = np.pad(labels_to_add, (0, max_len -
                            labels_to_add.size), constant_values=0)
            report[str(val)] = np.where(padded == 0, np.nan, padded)
            start_idx = end_idx
        report_out = pd.DataFrame(report)

        print(f"{report_header}\n{sep_long}\n{report_out}")

        save = input("Save current report? [y/n]")
        if save == 'y':
            save_path = input(
                "Please enter a full path (with .csv suffix) for saving the report:")
            report_out.to_csv(save_path)
        else:
            pass

        return


# ----------------------- script body -----------------------

tracked_objects_infos = {}

if opts.dqn:
    opts.game = opts.game
    opts.path = f"models/{opts.game}/dqn.gz"
    try:
        dqn_agent = load_agent(opts, env.action_space.n)
    except FileNotFoundError:
        oc_atari_dir = pathlib.Path(__file__).parents[1].resolve()
        opts.path = str(oc_atari_dir / 'models' / f"{opts.game}" / 'dqn.gz')
        dqn_agent = load_agent(opts, env.action_space.n)

ram_saves = []      # ram states
diff_saves = []     # number of image pixel differences
obj_extents = []    # surface areas of the tracked object (bbox width x height)
prop_saves = []     # values of the tracked property
base_obs, _, _, _, _ = env.step(0)
cat = opts.tracked_objects[0]       # tracked object category

if opts.snapshot:
    snapshot = pickle.load(open(opts.snapshot, "rb"))
    env._env.env.env.ale.restoreState(snapshot)
else:
    observation, info = env.reset()

# data acquisition run

for i in tqdm(range(opts.nb_samples)):
    # obs, reward, terminated, truncated, info = env.step(random.randint(0, env.action_space.n-1))
    if opts.dqn:
        action = dqn_agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, env.nb_actions-1)

    obs, reward, terminated, truncated, info = env.step(action)

    n_pixel_diff = np.sum(obs != base_obs) // 3
    diff_saves.append(n_pixel_diff)
    base_obs = obs

    ram = env.get_ram()
    save = True

    for objstr in opts.tracked_objects:
        if str(env.objects).count(f"{objstr} at") != 1:
            save = False  # don't save anything
    current_objects = dict([(obj.category, obj) for obj in env.objects])
    if cat in current_objects.keys():
        obj = current_objects[cat]
        new_prop = obj.__getattribute__(opts.tracked_properties[0])
        surf = obj.w * obj.h
        prop_saves.append(new_prop)
        obj_extents.append(surf)
    if not save:
        continue

    ram_saves.append(deepcopy(ram))

    if terminated or truncated:
        observation, info = env.reset()
        if opts.snapshot:
            env._env.env.env.ale.restoreState(snapshot)

    # modify and display render

env.close()

# Here, the maximum number of differences between two consecutive images, plus an arbitrary margin, is used to detect ram manipulations
# that cause game-crashes. If this causes false positive interactions with the tracked property, the value-pair candidate is discarded.
# Though, there may be better approaches than this very basic empirical one. While checking the results, some value-pairs do have unwanted
# interactions e.g., splitting another game object in half, which is not detected by the current approach.

img_diff_ceil = max(diff_saves) * (1 + diff_headroom)
obj_diff_ceil = max(diff_saves) * 2

ram_saves = np.array(ram_saves).T
from_rams = {str(i): ram_saves[i] for i in range(
    128) if not np.all(ram_saves[i] == ram_saves[i][0])}

df = pd.DataFrame(from_rams)
# find correlation
corr = df.corr(method=opts.method)

# Reduce the correlation matrix
# subset = tracked_objects_infos
# [f"{obj}_x" for obj in opts.tracked_objects] + [f"{obj}_y" for obj in opts.tracked_objects]
print("-"*20)
for el, onlynans in corr.isna().all(axis=1).items():
    if onlynans:
        print(
            f"Only NaNs found for {el} in the correlation matrix, most probably fix attribute.")
print("-"*20)
# Use submatrice

viz_correlations(corr)
ram_pairs, corr_positions = find_corr_pairs(corr, opts.quantile)

tracker = InteractionTracker(env, obj_cat=opts.tracked_objects[0], property=opts.tracked_properties[0],
                             ram_data=df, high_corrs=ram_pairs, positions=corr_positions)

interactions = tracker.test_all_ram_pairs(obj_diff_ceil)
props_generated = np.concatenate(
    tuple([candidate.get_prop_values() for candidate in interactions]))

compare_prop_stats(prop_saves, props_generated)

tracker.plot_interaction_summary()
tracker.create_interaction_report()
