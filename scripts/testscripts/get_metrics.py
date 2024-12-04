# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa


import random
import matplotlib.pyplot as plt
# sys.path.insert(0, '../ocatari') # noqa
from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.tennis import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.vision.bowling import objects_colors
from ocatari.vision.breakout import objects_colors
from ocatari.utils import load_agent, test_parser, make_deterministic, RandomAgent
from copy import deepcopy
import numpy as np
import os
import json
from termcolor import colored
from pyfiglet import Figlet
from tqdm import tqdm
import pandas as pd

import functools as ft

from metrics_utils import *
import pickle
import sys, inspect


figlet = Figlet()
report_bad = {}
all_stats = []
opts = test_parser.parse_args()
if opts.seed:
    make_deterministic(opts.seed)
game_name = opts.game
SAVE_FOLDER = "reports"
SAVE_IMAGE_FOLDER = f"{SAVE_FOLDER}/{game_name}"
os.makedirs(SAVE_IMAGE_FOLDER, exist_ok=True)
print(colored(figlet.renderText(f"Testing  {game_name}"), "blue"))
MODE = "both"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array', obs_mode='dqn')
observation, info = env.reset()
game_name = game_name.split("/")[-1]
NB_SAMPLES = 500

MIN_ACCEPTABLE_IOU = 0.5

print(colored(f'Using {MIN_ACCEPTABLE_IOU} as iou threshold for the saved images..', "magenta"))



ONLYBOTHDEFINEDOBJECTS = True
if ONLYBOTHDEFINEDOBJECTS:
    classes = []
    for mode in ["ram", "vision"]:
        mod_path = f"ocatari.{mode}.{game_name.lower()}"
        classes.append([el[0] for el in inspect.getmembers(sys.modules[mod_path], inspect.isclass)])
    classes_in_both = set.intersection(set(classes[0]) & set(classes[1]))


opts.path = f"models/{opts.game}/dqn.gz"
dqn_agent = load_agent(opts, env.action_space.n)
# dqn_agent = None
opts.path = f"models/{opts.game}/c51.gz"
try:
    c51_agent = load_agent(opts, env.action_space.n)
except FileNotFoundError:
    c51_agent = None
random_agent = RandomAgent(env.action_space.n)
im_reports = ""
fig, axes = plt.subplots(1, 3, figsize=(20, 10))
df_finals = []
detections_scores = []
agents = [random_agent, dqn_agent, c51_agent]
for agent, meth_name in zip(agents, ["Random", "DQN", "C51"]):
    if agent is not None:
        ALL_STATS = {
                "mean_ious": [],
                "per_class_ious": {},
                "only_in_ram": {},
                "only_in_vision": {},
                "dets": {}
                }
        det_scores = DetectionScores()
        with tqdm(total=NB_SAMPLES) as pbar:
            pbar.set_description(f"Testing {opts.game}")
            for i in range(20*NB_SAMPLES):
                action = agent.draw_action(env.dqn_obs)
                obse, reward, terminated, truncated, info = env.step(action)
                if i % 20 == 0:
                    if ONLYBOTHDEFINEDOBJECTS:
                        robjects = [e for e in env.objects if e.__class__.__name__ in classes_in_both]
                        vobjects = [e for e in env.objects_v if e.__class__.__name__ in classes_in_both]
                    else:
                        robjects = env.objects
                        vobjects = env.objects_v
                    stats = get_all_metrics(robjects, vobjects)
                    det_scores.update(stats["dets"])
                    ALL_STATS["mean_ious"].append(stats["mean_iou"])
                    for class_name, value in stats["per_class_ious"].items():
                        if not class_name in ALL_STATS["per_class_ious"]:
                            ALL_STATS["per_class_ious"][class_name] = []
                        ALL_STATS["per_class_ious"][class_name].append(value)
                    for only_in in ["only_in_ram", "only_in_vision"]:
                        for obj in stats[only_in]:
                            if not class_name in ALL_STATS[only_in]:
                                ALL_STATS[only_in][class_name] = 0
                            ALL_STATS[only_in][class_name] += 1
                    if stats["mean_iou"] < MIN_ACCEPTABLE_IOU:
                        obse2 = deepcopy(obse)
                        obss = []
                        for ax, obs, objects_list, title in zip(axes, [obse, obse2],
                                                                [robjects, vobjects],
                                                                ["ram", "vision"]):
                            for obj in objects_list:
                                opos = obj.xywh
                                ocol = obj.rgb
                                sur_col = make_darker(ocol)
                                mark_bb(obs, opos, color=sur_col)
                                # mark_point(obs, *opos[:2], color=(255, 255, 0))
                            ax.imshow(obs)
                            ax.set_title(title)
                            obss.append(obs)
                        for ax in axes.flatten():
                            ax.set_xticks([])
                            ax.set_yticks([])
                        # plt.imshow(obse)
                        # plt.show()
                        image_n = i // 20
                        axes[2].imshow(obss[1] - obss[0])
                        axes[2].set_title("difference")
                        plt.tight_layout()
                        plt.savefig(f"{SAVE_IMAGE_FOLDER}/{game_name}_{meth_name}_{image_n}.png")
                        # plt.show()
                        # print(env.objects)
                        # print(env.objects_v)
                        fig, axes = plt.subplots(1, 3, figsize=(20, 10))
                        im_reports += f"{image_n} (iou={stats['mean_iou']:.3f}),  "
                        report_bad[f"Image_{image_n}"] = stats
                    pbar.update(1)

                if terminated or truncated:
                    observation, info = env.reset()
                # modify and display render
        # pbar.close()
        env.close()
        ALL_STATS["mean_ious"] = np.nanmean(ALL_STATS["mean_ious"])
        for class_name, value in ALL_STATS["per_class_ious"].items():
            ALL_STATS["per_class_ious"][class_name] = np.mean(value)
        for only_in in ["only_in_ram", "only_in_vision"]:
            for obj_name, value in ALL_STATS[only_in].items():
                ALL_STATS[only_in][obj_name] = f"{value}/{NB_SAMPLES}"


        json_report_bad = json.dumps(report_bad, indent=4)
        json_report_bad = f"Details of frames with mean iou < {MIN_ACCEPTABLE_IOU}\n" + json_report_bad
        with open(f"{SAVE_FOLDER}/report_bad_{game_name}_{meth_name}.json", "w") as outfile:
            outfile.write(json_report_bad)
        json_all_stats = json.dumps(ALL_STATS, indent=4)
        with open(f"{SAVE_FOLDER}/all_stats_{game_name}_{meth_name}.json", "w") as outfile:
            outfile.write(json_all_stats)

        print_all_stats(ALL_STATS)
        print(f"Saved report_bad_{game_name}_{meth_name}.json and all_stats_{game_name}_{meth_name}.json in {SAVE_FOLDER}")


        if im_reports:
            print(f"Saved the following images with iou < {MIN_ACCEPTABLE_IOU}:\n" + im_reports + f"\n in {SAVE_IMAGE_FOLDER}")
            print(f"Saved {SAVE_FOLDER}/report_bad_{game_name}_{meth_name}.json for details on these images")

        ious = ALL_STATS['per_class_ious']
        names = [n.replace("_", " ") for n in ious.keys()]
        # ious_dfs.append(pd.DataFrame(format_values(ious.values()), index=names, columns=[meth_name]))
        # df = pd.DataFrame(format_values(ious.values()), index=names, columns=[meth_name])
        dfs = []
        dfs.append(pd.DataFrame.from_dict(format_values(det_scores.cat_precisions), orient="index", columns=["Precision"]))
        dfs.append(pd.DataFrame.from_dict(format_values(det_scores.cat_recalls), orient="index", columns=["Recall"]))
        dfs.append(pd.DataFrame.from_dict(format_values(det_scores.cat_f_scores), orient="index", columns=["F-score"]))
        dfs.append(pd.DataFrame.from_dict(format_values(ious), orient="index", columns=["IOU"]))
        df_finals.append(ft.reduce(lambda left, right: pd.DataFrame.join(left, right), dfs))
        det_scores.iou = ALL_STATS["mean_ious"]
        print(f"\nPrecision: {format_values(det_scores.cat_precisions)}")
        print(f"\nRecalls: {format_values(det_scores.cat_recalls)}")
        print(f"\nF-Scores: {format_values(det_scores.cat_f_scores)}")
        detections_scores.append(det_scores)
    else:
        df_finals.append(pd.DataFrame(columns=['Precision', 'Recall', 'F-score', 'IOU']))

# exit()
df = pd.concat(df_finals, axis=1, keys=["Random", "DQN", "C51"])
styler = df.style
styler.background_gradient(cmap="RdYlGn", vmin=0, vmax=100)
styler.format(precision=1)
ltx_code = styler.to_latex(
    caption=f"Per class IOU on {game_name}",
    clines="skip-last;data",
    convert_css=True,
    position_float="centering",
    hrules=True,
    multicol_align="c"
)

ltx_code = ltx_code.replace("100.0", "100").replace("\n & 0 \\\\\n\\midrule", "")
ltx_code = ltx_code.replace("lrrrrrrrrrrr", "l|rrrr|rrrr|rrrr").replace("multicolumn{4}{c}{Random}", "multicolumn{4}{c|}{Random}")

texf = "reports/latex"
os.makedirs(texf, exist_ok=True)
with open(f'{texf}/{game_name}_stat_reports.tex', 'w') as texfile:
    texfile.write(ltx_code)

print(f'Saved latex report in  {texf}/{game_name}_stat_reports.tex')
pkl_report_file = "reports/all_games_report.pkl"
already = None
if os.path.exists(pkl_report_file):
    with open(pkl_report_file, "rb") as savefile:
        already = pickle.load(savefile)


base_dfs = []
for det_scores, agent in zip(detections_scores, agents):
    if agent is not None:
        base_dfs.append(pd.DataFrame.from_dict(det_scores.dict_summary, orient="index", columns=[opts.game]).T * 100)
    else:
        base_dfs.append(pd.DataFrame(columns=['precision', 'recall', 'f-score', 'iou']))
stats = pd.concat(base_dfs, axis=1, keys=["Random", "DQN", "C51"])
stats = stats.round(1)
if already is not None:
    stats = pd.concat([already, stats]).sort_index()

stats.groupby(stats.index).aggregate(max)

with open(pkl_report_file, "wb") as savefile:
    pickle.dump(stats, savefile)
print(f"Updated {pkl_report_file}")