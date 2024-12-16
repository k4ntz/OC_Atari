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
import ipdb  # noqa
import pathlib
from termcolor import colored
import pickle
from ocatari.core import OCAtari
sys.path.insert(0, '../ocatari')  # noqa


def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=50, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10)
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()


def append_oinfo_values(obj, object_infos, objects_correctly_detected):
    name = obj.__class__.__name__
    # print(name)
    if f"{name}_x" in object_infos.keys() and f"{name}_x" not in objects_correctly_detected:
        object_infos[f"{name}_x"].append(obj.x)
        object_infos[f"{name}_y"].append(obj.y)
        objects_correctly_detected.append(f"{name}_x")
        objects_correctly_detected.append(f"{name}_y")


def generate_dataset(env, drop_constants, frames=700, skip_frames=3, manipulated_ram=None, start_frame=0):
    """
    generates test Data in the given environment(env) for the given objects(object_list)
    """
    ram_saves = []
    manipulated_ram_saves = []  # only if manipulated_ram is not None
    constants = {}
    prev_ram = None
    env.step(env.action_space.sample())
    for i in range(start_frame):
        env.step(env.action_space.sample())

    object_infos = {}
    for obj in env.objects:
        name = obj.__class__.__name__
        object_infos[f"{name}_x"] = []
        object_infos[f"{name}_y"] = []

    for i in tqdm(range(frames)):
        if manipulated_ram is not None:
            rand = random.randint(40, 100)
            env._env.unwrapped.ale.setRAM(manipulated_ram, rand)

        # obs, reward, terminated, truncated, info = env.step(env._env.action_space.sample())
        obs, reward, terminated, truncated, info = env.step(
            env.action_space.sample())

        if info.get('frame_number') > 10 and i % skip_frames == 0:

            objects_correctly_detected = []
            skip = False
            for obj_name in object_infos.keys():
                obj = obj_name[:-2]
                if not any(obj == x.__class__.__name__ for x in env.objects):
                    # object_infos[obj_name].append(0)  # not good but best workaround i could come up with
                    print(colored(str(obj) + " not from vision detected", "red"))
                    skip = True
                    break
            if skip:
                continue

            for obj in env.objects:
                append_oinfo_values(obj, object_infos,
                                    objects_correctly_detected)

            ram = env._env.unwrapped.ale.getRAM()
            ram_saves.append(deepcopy(ram))
            if manipulated_ram is not None:
                manipulated_ram_saves.append(ram[manipulated_ram])
            if prev_ram is not None:
                new_constants = {}
                for c, v in constants.items():
                    if ram[c] == prev_ram[c]:
                        new_constants.update({c: v})
                constants = new_constants
            else:
                for u in range(len(ram)):
                    constants.update({u: ram[u]})
            prev_ram = ram
            # env.render()
        # modify and display render
    if manipulated_ram is not None:
        from_rams = {str(manipulated_ram): manipulated_ram_saves}
        object_infos.update(from_rams)

        return object_infos

    ram_saves = np.array(ram_saves).T
    if drop_constants:
        from_rams = {str(i): ram_saves[i] for i in range(
            128) if not np.all(ram_saves[i] == ram_saves[i][0])}
    else:
        from_rams = {str(i): ram_saves[i] for i in range(128)}

    objects = list(object_infos.keys())
    object_infos.update(from_rams)

    return object_infos, constants, objects


def get_correlation(dataset, min_correlation, objects, method="pearson"):
    """
    methods: "spearman","kendall","pearson"
    """
    df = pd.DataFrame(dataset)
    corr = df.corr(method=method)
    # Reduce the correlation matrix
    # subset = [f"{obj}_x" for obj in env.objects] + [f"{obj}_y" for obj in object_list]
    subset = objects

    # Use submatrice
    corr = corr[subset].T
    corr.drop(subset, axis=1, inplace=True)

    corr = corr[corr.columns[corr.abs().max() > min_correlation]]

    return corr


def dump_heatmap(correlation, filename, game_name):
    ax = sns.heatmap(correlation, vmin=-1, vmax=1, annot=True,
                     cmap=sns.diverging_palette(20, 220, n=200))

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


def do_analysis(env, dump_path, new_dump, min_correlation, maximum_x,
                maximum_y, drop_constants, start_frame=0):
    # ---------------------------test-data-dump-------------------------------
    game_name = env.game_name
    if dump_path is None:
        dump_path = str(pathlib.Path().resolve()) + \
            "/../dumps/automated_analysis_dump/"
    if not os.path.exists(dump_path):
        os.makedirs(dump_path)
    dump_path = dump_path + game_name
    if not os.path.exists(dump_path):
        os.makedirs(dump_path)

    oinfo_file = dump_path + "/object_infos"
    constants_file = dump_path + "/constants"
    objects_file = dump_path + "/objects"
    if (not os.path.exists(oinfo_file)) or new_dump:
        dataset, constants, objects = generate_dataset(
            env, drop_constants, start_frame=start_frame)
        with open(oinfo_file, 'wb+') as f:
            pickle.dump(dataset, f)
        with open(constants_file, 'wb+') as f:
            pickle.dump(constants, f)
        with open(objects_file, 'wb+') as f:
            pickle.dump(objects, f)
    else:
        with open(oinfo_file, 'rb') as f:
            dataset = pickle.load(f)
        with open(constants_file, 'rb') as f:
            constants = pickle.load(f)
        with open(objects_file, 'rb') as f:
            objects = pickle.load(f)

    # -------------------------------------------------------------------------
    corr = get_correlation(dataset, min_correlation, objects)
    dump_heatmap(corr, dump_path + "/correlation_heatmap", game_name)
    candidates = corr.T.to_dict()

    cand_file = dump_path + "/approved_candidates"
    if (not os.path.exists(cand_file)) or new_dump:
        approved_candidates = {}
        for obj_name in objects:
            print(obj_name)
            candidates[obj_name] = {
                k: v for k, v in candidates[obj_name].items() if abs(v) > min_correlation}
            print(candidates[obj_name])
            approved_candidates[obj_name] = []
            if len(candidates[obj_name]) > 1:
                for ram_pos in candidates[obj_name]:
                    env.reset()
                    dataset2 = generate_dataset(env, drop_constants,
                                                frames=300, manipulated_ram=int(ram_pos), start_frame=start_frame)
                    if obj_name in dataset2:
                        dataset2[obj_name] = np.array(dataset2[obj_name])

                        if len(dataset2[ram_pos]) > 0 and not (np.all(dataset2[ram_pos] == dataset2[ram_pos][0]) or
                                                               np.all(dataset2[obj_name] == dataset2[obj_name][0])):
                            corr2 = np.corrcoef(
                                dataset2[obj_name], dataset2[ram_pos])[1][0]
                            approved_candidates[obj_name].append({"pos": int(ram_pos),
                                                                  "corr": candidates[obj_name][ram_pos],
                                                                  "manipulated_corr": corr2})

                def s(d):
                    return abs(d["manipulated_corr"])

                approved_candidates[obj_name].sort(key=s, reverse=True)

            else:
                for k in candidates[obj_name]:
                    # is there a way to extract key value with unknown key without iterating?
                    approved_candidates[obj_name].append(
                        {"pos": int(k), "corr": candidates[obj_name][k], "manipulated_corr": None})

        with open(cand_file, 'wb+') as f:
            pickle.dump(approved_candidates, f)
    else:
        with open(cand_file, 'rb') as f:
            approved_candidates = pickle.load(f)

    # ---------print out constants----------
    print(constants)
    print("constants: ")
    prev_c = None
    constant_str = ""
    for c, v in constants.items():
        if prev_c is None:
            constant_str = str(c) + ": " + str(v)

        elif prev_c + 1 == c:
            constant_str = constant_str + ",  " + str(c) + ": " + str(v)

        else:
            print(constant_str)
            constant_str = str(c) + ": " + str(v)
        prev_c = c

    print(constant_str)
    constant_str = "\n["
    for c, v in constants.items():
        constant_str = constant_str + str(c) + ", "

    constant_str = constant_str[:-2] + "]"
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
    GAME_NAME = "Riverraid-v4"
    MODE = "vision"    # do not change
    RENDER_MODE = "rgb_array"  # do not change
    MAXIMUM_X = 160  # right side of screen in rgb_array
    MAXIMUM_Y = 210  # bottom of screen in rgb_array
    DUMP_PATH = None  # path to dump otherwise takes standard
    NEW_DUMP = True  # if True creates new datasets and dumps it overwriting the previous ones
    # the minimal correlation required for a ram value to be relevant for an object
    MIN_CORRELATION = 0.8
    DROP_CONSTANTS = True  # if True does not consider not changing variables for objects
    START_FRAME = 100  # selects the frame at which each simulation starts

    env = OCAtari(GAME_NAME, mode=MODE, render_mode=RENDER_MODE)
    random.seed(0)
    observation, info = env.reset()
    obs, reward, terminated, truncated, info = env.step(
        env.action_space.sample())
    env.reset()

    do_analysis(env, drop_constants=DROP_CONSTANTS, dump_path=DUMP_PATH,
                new_dump=NEW_DUMP, min_correlation=MIN_CORRELATION,
                maximum_x=MAXIMUM_X, maximum_y=MAXIMUM_Y, start_frame=START_FRAME)

    env.close()
