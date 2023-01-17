"""
An attempt to change quentins code (find_correlation) to require minimal human interaction
"""
import sys
import os

import random
import matplotlib.pyplot as plt
from copy import deepcopy
from tqdm import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import RANSACRegressor, LinearRegression
import ipdb # noqa
import pathlib
from termcolor import colored
import pickle
sys.path.insert(0, '../ocatari') # noqa
from core import OCAtari
from vision.freeway import objects_colors


def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=50, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10)
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()


def append_oinfo_values(obj_name, oinfo, object_infos):
    if type(oinfo) == tuple:
        object_infos[f"{obj_name}_x"].append(oinfo[0])
        object_infos[f"{obj_name}_y"].append(oinfo[1])

    elif type(oinfo) == list:
        index = 0
        for oinfoTuple in oinfo:
            obj_name_altered = str(obj_name) +str(index)
            index += 1
            object_infos[f"{obj_name_altered}_x"].append(oinfoTuple[0])
            object_infos[f"{obj_name_altered}_y"].append(oinfoTuple[1])


def generate_dataset(env, object_list, drop_constants, frames=400, skip_frames=3, manipulated_ram=None, ):
    """
    generates test Data in the given environment(env) for the given objects(object_list)
    """
    object_infos = {}
    for obj in object_list:
        object_infos[f"{obj}_x"] = []
        object_infos[f"{obj}_y"] = []
    ram_saves = []
    manipulated_ram_saves = []  # only if manipulated_ram is not None
    constants = {}
    prevRam = None
    env.step(0)
    for i in tqdm(range(frames)):
        if manipulated_ram is not None:
            rand = random.randint(40, 100)
            env._env.unwrapped.ale.setRAM(manipulated_ram, rand)

        obs, reward, terminated, truncated, info = env.step(env._env.action_space.sample())

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
                append_oinfo_values(obj_name, oinfo, object_infos)
            ram = env._env.unwrapped.ale.getRAM()
            ram_saves.append(deepcopy(ram))
            if manipulated_ram is not None:
                manipulated_ram_saves.append(ram[manipulated_ram])
            if prevRam is not None:
                new_constants = {}
                for c, v in constants.items():
                    if ram[c] == prevRam[c]:
                        new_constants.update({c: v})
                constants = new_constants
            else:
                for i in range(len(ram)):
                    constants.update({i: ram[i]})
            prevRam = ram
            # env.render()

        # modify and display render
    if manipulated_ram is not None:
        from_rams = {str(manipulated_ram): manipulated_ram_saves}
        object_infos.update(from_rams)

        return object_infos

    ram_saves = np.array(ram_saves).T
    if drop_constants:
        from_rams = {str(i): ram_saves[i] for i in range(128) if not np.all(ram_saves[i] == ram_saves[i][0])}
    else:
        from_rams = {str(i): ram_saves[i] for i in range(128)}

    object_infos.update(from_rams)

    return object_infos, constants


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


def calculate_offset(vision, ram, corr, pos, maximum=160):
    """
    calculates possible offsets between what is displayed and what is stored in the ram
    """
    offset_list = []
    for i in range(len(vision)):
        if corr < 0:
            diff = vision[i] - (maximum - ram[i])
            offset_list.append(maximum + diff)
        else:
            diff = vision[i] - ram[i]
            offset_list.append(diff)

    offset_list = list(dict.fromkeys(offset_list))  # remove duplicates
    offset_string = ""
    for offset in offset_list:
        c = " + "
        if corr < 0:
            c = " - "
        offset_string = offset_string + str(offset) + c + "ram[" + pos + "], "
    return offset_string


def do_analysis(env, object_list, dump_path, new_dump, min_correlation, maximum_x,
                maximum_y, drop_constants):
    # ---------------------------test-data-dump-------------------------------
    game_name = env.game_name
    if dump_path is None:
        dump_path = str(pathlib.Path().resolve()) + "/../dumps/automated_analysis_dump/"
    if not os.path.exists(dump_path):
        os.mkdir(dump_path)
    dump_path = dump_path + game_name
    if not os.path.exists(dump_path):
        os.mkdir(dump_path)

    oinfo_file = dump_path + "/object_infos"
    constants_file = dump_path + "/constants"
    if (not os.path.exists(oinfo_file)) or new_dump:
        dataset, constants = generate_dataset(env, object_list, drop_constants)
        with open(oinfo_file, 'wb+') as f:
            pickle.dump(dataset, f)
        with open(constants_file, 'wb+') as f:
            pickle.dump(constants, f)
    else:
        with open(oinfo_file, 'rb') as f:
            dataset = pickle.load(f)
        with open(constants_file, 'rb') as f:
            constants = pickle.load(f)

    # -------------------------------------------------------------------------
    corr = get_correlation(dataset, min_correlation=min_correlation)
    dump_heatmap(corr, dump_path + "/correlation_heatmap", game_name)
    candidates = corr.T.to_dict()

    cand_file = dump_path + "/approved_candidates"
    if (not os.path.exists(cand_file)) or new_dump:
        approved_candidates = {}
        for obj in object_list:
            for xy in ["_x", "_y"]:
                c = obj + xy
                candidates[c] = {k: v for k, v in candidates[c].items() if abs(v) > min_correlation}
                approved_candidates[c] = []
                if len(candidates[c]) > 1:
                    for ram_pos in candidates[c]:
                        env.reset()
                        dataset2 = generate_dataset(env, [obj], drop_constants,
                                                    frames=100, manipulated_ram=int(ram_pos))
                        dataset2[c] = np.array(dataset2[c])

                        if not (np.all(dataset2[ram_pos] == dataset2[ram_pos][0]) or
                                np.all(dataset2[c] == dataset2[c][0])):
                            corr2 = np.corrcoef(dataset2[c], dataset2[ram_pos])[1][0]
                            approved_candidates[c].append({"pos": int(ram_pos), "corr": candidates[c][ram_pos],
                                                           "manipulated_corr": corr2})

                    def s(d):
                        return abs(d["manipulated_corr"])

                    approved_candidates[c].sort(key=s, reverse=True)

                else:
                    for k in candidates[c]:  # is there a way to extract key value with unknown key without iterating?
                        approved_candidates[c].append(
                            {"pos": int(k), "corr": candidates[c][k], "manipulated_corr": None})

        with open(cand_file, 'wb+') as f:
            pickle.dump(approved_candidates, f)
    else:
        with open(cand_file, 'rb') as f:
            approved_candidates = pickle.load(f)

    # ---------print out constants----------
    print(constants)
    print("constants: ")
    prevC = None
    constant_str = ""
    for c, v in constants.items():
        if prevC is None:
            constant_str = str(c) + ": " + str(v)

        elif prevC + 1 == c:
            constant_str = constant_str + ",  " + str(c) + ": " + str(v)

        else:
            print(constant_str)
            constant_str = str(c) + ": " + str(v)
        prevC = c

    print(constant_str)

    # ---------print out candidates---------
    best_candidates = {}
    print("\n----------------------------------------------------------------\n")
    print(candidates)
    print("best candidates:")
    for cand, arr in approved_candidates.items():
        best_candidates.update({cand: []})
        for dictionary in arr:
            best_candidates[cand].append(dictionary["pos"])

    print(best_candidates)

    # ---------------------------------------
    print("\n----------------------------------------------------------------\n")
    print("possible offsets: ")
    for cand, arr in best_candidates.items():
        maximum = maximum_x
        if cand[len(cand) - 1] == 'y':
            maximum = maximum_y
        for pos in arr:
            offset_string = calculate_offset(dataset[cand], dataset[str(pos)],
                                             candidates[cand][str(pos)], str(pos), maximum=maximum)
            print(cand + "(" + str(pos) + "): " + offset_string)
        print("------------------------------------")


if __name__ == "__main__":
    GAME_NAME = "Kangaroo"
    MODE = "vision"    # do not change
    # RENDER_MODE = "human"
    RENDER_MODE = "rgb_array"  # do not change
    MAXIMUM_X = 160  # right side of screen in rgb_array
    MAXIMUM_Y = 210  # bottom of screen in rgb_array
    DUMP_PATH = None  # path to dump otherwise takes standard
    NEW_DUMP = True  # if True creates new datasets and dumps it overwriting the previous ones
    MIN_CORRELATION = 0.8
    DROP_CONSTANTS = True  # if True does not consider not changing variables for objects

    env = OCAtari(GAME_NAME, mode=MODE, render_mode=RENDER_MODE)
    random.seed(0)
    observation, info = env.reset()
    obs, reward, terminated, truncated, info = env.step(0)
    env.reset()

    object_list = info["objects"].keys()  # "ball_shadow"
    print("objects that will be analyzed: " + str(object_list))

    do_analysis(env, object_list, drop_constants=DROP_CONSTANTS, dump_path=DUMP_PATH,
                new_dump=NEW_DUMP, min_correlation=MIN_CORRELATION,
                maximum_x=MAXIMUM_X, maximum_y=MAXIMUM_Y)

    env.close()
