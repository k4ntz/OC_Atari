"""
This script allows to track bit changes and inspect bit activity in the ram.
"""

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
parser.add_argument("-tn", "--top_n", type=int, default=3,
                    help="The top n value to be kept in the correlation matrix")
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
parser.add_argument("-ia", "--interactive", action="store_true",
                    help="Interactive mode for scrolling through frames and ram changes.")
opts = parser.parse_args()


def create_bitmats(ram_saves):
    """Returns a matrices with binary representations of the ram values in binary and decimal."""

    bit_depth = 8
    ram_depth = 256
    ram_width = ram_saves.shape[-1]

    n_frames = ram_saves.shape[0]

    bit_matrices = np.zeros((ram_saves.shape[0], bit_depth, ram_width))
    ram_matrices = np.zeros((ram_saves.shape[0], ram_depth, ram_width))

    for f in range(n_frames):
        ram_copy = deepcopy(ram_saves[f, :])

        bit_matrix = np.zeros((ram_width, bit_depth))
        ram_matrix = np.zeros((ram_width, ram_depth))

        for i in range(ram_width):
            ram_value = ram_copy[i]
            ram_matrix[i][ram_value] = 1
            bin_string = format(ram_value, 'b')
            # create bit vector of the ram value for the current position
            bit_array = np.array([int(d) for d in bin_string.zfill(bit_depth)])
            bit_matrix[i] = bit_array

        bit_matrices[f, :, :] = bit_matrix.T
        ram_matrices[f, :, :] = ram_matrix.T

    bit_mats = {'bin': bit_matrices, 'dec': ram_matrices}

    return bit_mats


def bit_correlation(bit_mats, tresh):

    frames, bit_pos, ram_pos = bit_mats.shape
    n_entries = bit_pos*ram_pos
    data = np.reshape(bit_mats, (frames, bit_pos*ram_pos))
    corr = np.zeros((n_entries, n_entries))
    for i in range(n_entries):
        series1 = data[:, i]
        for j in range(n_entries):
            if j % 128 == 0:
                continue
            series2 = data[:, j]
            score = np.count_nonzero(np.equal(series1, series2))
            corr[i, j] = score / frames

    corr[corr < tresh] = 0
    fig, ax = plt.subplots()
    img = plt.imshow(corr, aspect='auto', cmap='viridis', interpolation='none')

    ax.set_title("Correlation between individual bits")
    plt.colorbar(mappable=img, ax=ax, orientation='vertical',
                 fraction=.1, label='Correlation')

    return fig, ax


def remove_zero_cols(ram_saves):

    data = list()

    ram_saves_all = np.array(ram_saves['all'])
    t_collapsed = np.sum(ram_saves_all, axis=0)
    idx = np.argwhere(t_collapsed == 0)
    ram_labels = np.delete(np.arange(0, 128, 1), obj=idx, axis=0)

    for entry in ram_saves.values():
        m = np.array(entry)
        m_condensed = np.delete(m, obj=idx, axis=-1)
        data.append(m_condensed)

    collections = tuple(data)

    return collections, ram_labels


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

tracked_objects_infos = {}
for objname in opts.tracked_objects:
    for prop in opts.tracked_properties:
        tracked_objects_infos[f"{objname}_{prop}"] = []

subset = list(tracked_objects_infos.keys())

itest_ram_saves = []
itest_obs = []
ram_saves = dict((("obj", []), ("no_obj", []), ("all", [])))
categories = ram_saves.keys()
obs_saves = []

if opts.dqn:
    oc_atari_dir = pathlib.Path(__file__).parents[1].resolve()
    opts.path = str(oc_atari_dir / 'models' / f"{opts.game}" / 'dqn.gz')
    dqn_agent = load_agent(opts, env.action_space.n)

observation, info = env.reset()
if opts.snapshot:
    env._env.env.env.ale.restoreState(snapshot)


for i in tqdm(range(opts.nb_samples)):
    # obs, reward, terminated, truncated, info = env.step(random.randint(0, env.action_space.n-1))
    if opts.dqn:
        action = dqn_agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, env.nb_actions-1)
    obs, reward, terminated, truncated, info = env.step(action)

    ram = env.get_ram()

    ram_saves["all"].append(ram)

    for obj in env.objects:
        objname = obj.category
        if objname in opts.tracked_objects:
            ram_saves["obj"].append(ram)

            for prop in opts.tracked_properties:
                tracked_objects_infos[f"{objname}_{prop}"].append(
                    obj.__getattribute__(prop))
        else:
            ram_saves["no_obj"].append(ram)

    obs_saves.append(obs)

    if terminated or truncated:
        observation, info = env.reset()
        if opts.snapshot:
            env._env.env.env.ale.restoreState(snapshot)

    # modify and display render
env.close()

print(
    f"\nSaved {len(ram_saves['obj'])} frames with {opts.tracked_objects} present")
print(
    f"Saved {len(ram_saves['no_obj'])} frames with {opts.tracked_objects} absent")
# print(f"Found interactions for {opts.tracked_objects}_{opts.tracked_properties} for ram positions {list(interactions.keys())}")

obs_saves = np.array(obs_saves)

collections, active_positions = remove_zero_cols(ram_saves)
bit_mats = dict.fromkeys(categories, None)

for dataset, cat in zip(collections, categories):
    bit_mats[cat] = create_bitmats(dataset)


def plot_bit_activity(bit_mats_condensed, title):

    dBits = np.diff(bit_mats_condensed, axis=0)
    hist_mat = np.sum(np.abs(dBits), axis=0) / dBits.shape[0]
    fig, ax = plt.subplots()
    img = plt.imshow(hist_mat, aspect='auto',
                     cmap='viridis', interpolation='none')

    ax.set_xticks(
        np.arange(0, hist_mat.shape[1], 1.0), labels=active_positions)
    ax.tick_params(axis='x', labelrotation=90, labelsize=6)
    ax.set_title(title)
    plt.colorbar(mappable=img, ax=ax, orientation='vertical',
                 fraction=.1, label='Switch Frequency')

    return fig, ax


def compare_bit_mats(obj_saves, no_obj_saves):

    d_object_mats = np.diff(obj_saves, axis=0)
    d_no_object_mats = np.diff(no_obj_saves, axis=0)

    hist_mat_obj = np.sum(np.abs(d_object_mats), axis=0) / \
        d_object_mats.shape[0]
    hist_mat_no_obj = np.sum(np.abs(d_no_object_mats),
                             axis=0) / d_no_object_mats.shape[0]
    no_activity_mask = np.where(hist_mat_no_obj == 0, 1, 0)
    diff_map = hist_mat_obj * no_activity_mask
    data = (hist_mat_no_obj, hist_mat_obj, diff_map)
    titles = ("Tracked object absent", "Tracked object present",
              "Masked out inactive bits in 'absent' condition")
    fig, axs = plt.subplots(3, 1)

    for row, data, title in zip(axs, data, titles):
        img = row.imshow(data, aspect='auto', cmap='viridis',
                         interpolation='none')
        row.set_xticks(
            np.arange(0, data.shape[1], 1.0), labels=active_positions)
        row.tick_params(axis='x', labelrotation=90, labelsize=6)
        row.set_title(title)
        plt.colorbar(mappable=img, ax=row, orientation='vertical',
                     fraction=.1, label='Switch Frequency')

    fig.suptitle(
        f"Comparison of bitwise activity with respect to {opts.tracked_objects}", fontsize=20)
    fig.tight_layout()

    return fig, axs


class IndexTracker:
    def __init__(self, axs, bit_mats, game_imgs):
        self.index = 0
        self.axs = axs
        self.zero_cols = None
        self.bit_mats = bit_mats
        self.game_imgs = game_imgs
        self.ram_labels = active_positions
        self.dBits = np.diff(self.bit_mats, axis=0)
        self.max_index = self.bit_mats.shape[0] - 1

        a = axs['BITMAP']
        self.im2 = a.imshow(self.bit_mats[self.index, :, :], alpha=0.5,
                            aspect='auto', cmap='binary', interpolation='none', vmin=0, vmax=1)
        self.im = a.imshow(self.dBits[self.index, :, :], alpha=0.75,
                           aspect='auto', cmap='PiYG', interpolation='none', vmin=-1, vmax=1)
        a.set_xticks(np.arange(0, len(self.ram_labels), 1.0),
                     labels=self.ram_labels)
        a.tick_params(axis='x', labelrotation=90, labelsize=6)
        plt.colorbar(mappable=self.im, ax=a,
                     orientation='horizontal', fraction=.025)

        b = axs['PREV_IMG']
        self.im3 = b.imshow(self.game_imgs[self.index, :, :, :])
        c = axs['CURR_IMG']
        self.im4 = c.imshow(self.game_imgs[self.index + 1, :, :, :])
        d = axs['DIFF_IMG']
        self.im5 = d.imshow(
            self.game_imgs[self.index + 1, :, :, :] - self.game_imgs[self.index, :, :, :])

        self.update()

    def get_ram_labels(self):
        return self.ram_labels

    def get_dBits(self):
        return self.dBits

    def remove_zero_cols(self):
        t_collapsed = np.sum(np.sum(self.bit_mats, axis=0), axis=0)
        idx = np.argwhere(t_collapsed == 0)
        self.bit_mats = np.delete(self.bit_mats, obj=idx, axis=-1)
        self.ram_labels = np.delete(np.arange(0, 128, 1), obj=idx, axis=0)

    def on_press(self, event):
        increment = 1 if event.key == 'up' else -1
        self.index = np.clip(self.index + increment, 0, self.max_index)
        self.update()

    def update(self):
        self.im.set_data(self.dBits[self.index, :, :])
        self.im2.set_data(self.bit_mats[self.index, :, :])
        self.im3.set_data(self.game_imgs[self.index, :, :, :])
        self.im4.set_data(self.game_imgs[self.index + 1, :, :, :])
        self.im5.set_data(
            self.game_imgs[self.index + 1, :, :, :] - self.game_imgs[self.index, :, :, :])

        self.axs['BITMAP'].set_title(
            f'Use up/down buttons to navigate\nRAM changes from frame {self.index} to {self.index + 1}')
        self.axs['PREV_IMG'].set_title(f"Frame {self.index}")
        self.axs['CURR_IMG'].set_title(f"Frame {self.index + 1}")
        self.axs['DIFF_IMG'].set_title("Difference Image")

        self.im.axes.figure.canvas.draw()
        self.im2.axes.figure.canvas.draw()
        self.im3.axes.figure.canvas.draw()
        self.im4.axes.figure.canvas.draw()


fig4, ax4 = bit_correlation(bit_mats['all']['bin'], tresh=0.9)
fig2, ax2 = plot_bit_activity(
    bit_mats['all']['bin'], "Bit-Activity Across All Extracted RAM-States")
fig3, ax3 = compare_bit_mats(bit_mats['obj']['bin'], bit_mats['no_obj']['bin'])

if opts.interactive:
    ARR = [['BITMAP', 'BITMAP', 'BITMAP'],
           ['PREV_IMG', 'CURR_IMG', 'DIFF_IMG']]
    fig, axs = plt.subplot_mosaic(ARR)
    # create an IndexTracker and make sure it lives during the whole
    # lifetime of the figure by assigning it to a variable
    tracker = IndexTracker(axs, bit_mats['all']['bin'], obs_saves)

    fig.canvas.mpl_connect('key_press_event', tracker.on_press)

plt.show()
