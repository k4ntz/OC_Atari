"""
An attempt to change quentins code (find_correlation) to require minimal human interaction
"""
import os

from ocatari import OCAtari
import random
import matplotlib.pyplot as plt
from copy import deepcopy
from tqdm import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import RANSACRegressor, LinearRegression
# import ipdb
import pathlib
from termcolor import colored
import pickle


def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=50, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10)
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()


def generate_dataset(env, object_list, frames=600, skip_frames=3, manipulated_ram=None):
    """
    generates test Data in the given environment(env) for the given objects(object_list)
    """
    object_infos = {}
    for obj in object_list:
        object_infos[f"{obj}_x"] = []
        object_infos[f"{obj}_y"] = []
    ram_saves = []
    manipulated_ram_saves = []
    env.step(0)
    for i in tqdm(range(frames)):
        if manipulated_ram is not None:
            rand = random.randint(40, 100)
            env._env.unwrapped.ale.setRAM(manipulated_ram, rand)

        obs, reward, terminated, truncated, info = env.step(random.randint(0, 5))

        if info.get('frame_number') > 10 and i % skip_frames == 0:
            SKIP = False
            for obj_name in object_list:  # avoid state without the tracked objects
                if obj_name not in info["objects"]:
                    SKIP = True
                    print(colored(str(obj_name) + " not in info"))
                    break
            if SKIP:
                continue
            for obj_name in object_list:
                oinfo = info["objects"][obj_name]
                object_infos[f"{obj_name}_x"].append(oinfo[0])
                object_infos[f"{obj_name}_y"].append(oinfo[1])
            ram = env._env.unwrapped.ale.getRAM()
            ram_saves.append(deepcopy(ram))
            if manipulated_ram is not None:
                manipulated_ram_saves.append(ram[manipulated_ram])
            # env.render()

        # modify and display render
    if manipulated_ram is not None:
        from_rams = {str(manipulated_ram): manipulated_ram_saves}
        object_infos.update(from_rams)

        return object_infos

    ram_saves = np.array(ram_saves).T
    from_rams = {str(i): ram_saves[i] for i in range(128) if not np.all(ram_saves[i] == ram_saves[i][0])}

    object_infos.update(from_rams)

    return object_infos


def get_correlation(dataset, min_correlation, method="pearson"):
    """
    methods: "spearman","kendall","pearson"
    """
    df = pd.DataFrame(dataset)
    corr = df.corr(method=method)
    # Reduce the correlation matrix
    subset = [f"{obj}_x" for obj in object_list] + [f"{obj}_y" for obj in object_list]

    # Use submatrice
    corr = corr[subset].T
    corr.drop(subset, axis=1, inplace=True)

    corr = corr[corr.columns[corr.abs().max() > min_correlation]]

    return corr


def dump_heatmap(correlation, filename, game_name):
    ax = sns.heatmap(correlation, vmin=-1, vmax=1, annot=True, cmap=sns.diverging_palette(20, 220, n=200))

    for tick in ax.get_yticklabels():
        tick.set_rotation(0)

    xlabs = correlation.columns.to_list()
    plt.xticks(list(np.arange(0.5, len(xlabs) + .5, 1)), xlabs)
    plt.title(game_name)
    plt.savefig(filename)


def do_analysis(env, object_list, dump_path=None, new_dump=False, min_correlation=0.7):
    # ---------------------------test-data-dump-------------------------------
    game_name = env.game_name
    if dump_path is None:
        dump_path = str(pathlib.Path().resolve()) + "/dumps/automated_analysis_dump/" + game_name
    if not os.path.exists(dump_path):
        os.mkdir(dump_path)

    oinfo_file = dump_path + "/object_infos"
    if (not os.path.exists(oinfo_file)) or new_dump:
        dataset = generate_dataset(env, object_list)
        with open(oinfo_file, 'wb+') as f:
            pickle.dump(dataset, f)
    else:
        with open(oinfo_file, 'rb') as f:
            dataset = pickle.load(f)

    # -------------------------------------------------------------------------
    corr = get_correlation(dataset, min_correlation=min_correlation)
    print(corr)
    dump_heatmap(corr, dump_path+"/correlation_heatmap", game_name)
    candidates = corr.T.to_dict()
    approved_candidates = {}
    for obj in object_list:
        for xy in ["_x", "_y"]:
            c = obj + xy
            candidates[c] = {k: v for k, v in candidates[c].items() if v > min_correlation}
            approved_candidates[c] = []

            if len(candidates[c]) > 1:
                for ram_pos in candidates[c]:
                    env.reset()
                    dataset = generate_dataset(env, [obj], frames=100, manipulated_ram=int(ram_pos))
                    dataset[c] = np.array(dataset[c])

                    if not (np.all(dataset[ram_pos] == dataset[ram_pos][0]) or
                            np.all(dataset[c] == dataset[c][0])):
                        corr = np.corrcoef(dataset[c], dataset[ram_pos])[1][0]
                        approved_candidates[c].append({"pos": int(ram_pos), "corr": candidates[c][ram_pos],
                                                       "manipulated_corr": corr})

                def s(d):
                    return abs(d["manipulated_corr"])

                approved_candidates[c].sort(key=s, reverse=True)

            else:
                for k in candidates[c]:   # is there a way to extract key value with unknown key without iterating?
                    approved_candidates[c].append(
                        {"pos": int(k), "corr": candidates[c][k], "manipulated_corr": None})

    # ---------print out candidates---------
    print(candidates)
    print("best candidates:")
    for cand, arr in approved_candidates.items():
        canditateString = ""
        for dictionary in arr:
            canditateString = canditateString + str(dictionary["pos"])
        print(str(cand)+": "+canditateString)

    # ---------------------------------------


if __name__ == "__main__":
    GAME_NAME = "TennisDeterministic-v0"
    MODE = "vision"
    # RENDER_MODE = "human"
    RENDER_MODE = "rgb_array"

    env = OCAtari(GAME_NAME, mode=MODE, render_mode=RENDER_MODE)
    random.seed(0)
    observation, info = env.reset()

    object_list = ["ball", "enemy", "player", "ball_shadow"]

    do_analysis(env, object_list)

    env.close()
