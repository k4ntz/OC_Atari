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
from ocatari.utils import load_agent, test_parser
from copy import deepcopy
import numpy as np
import os
import json


def get_iou(obj1, obj2):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(obj1.x, obj2.x)
    yA = max(obj1.y, obj2.y)
    xB = min(obj1.x+obj1.w, obj2.x+obj2.w)
    yB = min(obj1.y+obj1.h, obj2.y+obj2.h)
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA) * max(0, yB - yA)
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (obj1.w) * (obj1.h)
    boxBArea = (obj2.w) * (obj2.h)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    # return the intersection over union value
    return iou


def difference_objects(ram_list, vision_list):
    only_in_ram = []
    only_in_vision = []
    per_class_ious = {}
    ious = []
    if abs(len(vision_list) - len(ram_list)) > 10:
        import ipdb; ipdb.set_trace()
    for vobj in vision_list:
        vobj._is_in_ram = False
    for robj in ram_list:
        robj._is_in_image = False
        for vobj in vision_list:
            if robj.__class__.__name__ == vobj.__class__.__name__:
                objname = robj.__class__.__name__
                iou = get_iou(robj, vobj)
                if iou > 0:
                    ious.append(iou)
                    if objname not in per_class_ious:
                        per_class_ious[objname] = [iou]
                    else:
                        per_class_ious[objname].append(iou)
                    vobj._is_in_ram = True
                    robj._is_in_image = True
                    break
    for name, li in per_class_ious.items():
        per_class_ious[name] = np.mean(li)
    for robj in ram_list:
        if not robj._is_in_image:
            only_in_vision.append(str(robj))
    for vobj in vision_list:
        if not vobj._is_in_ram:
            only_in_vision.append(str(vobj))
    return {"mean_iou": np.mean(ious), "per_class_ious": per_class_ious,
            "only_in_ram": only_in_ram, "only_in_vision": only_in_vision}


report_bad = {}
all_stats = []
SAVE_IMAGE_FOLDER = "diff_images"
os.makedirs(SAVE_IMAGE_FOLDER, exist_ok=True)
opts = test_parser.parse_args()
game_name = opts.game
MODE = "test"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()
NB_SAMPLES = 100
ALL_STATS = {
             "mean_ious": [],
             "per_class_ious": {},
             "only_in_ram": {},
             "only_in_vision": {}
             }
MIN_ACCEPTABLE_IOU = 0.8

if opts.path:
   agent = load_agent(opts, env.action_space.n)


fig, axes = plt.subplots(1, 2)
for i in range(NB_SAMPLES):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, 5)
    obse, reward, terminated, truncated, info = env.step(action)
    stats = difference_objects(env.objects, env.objects_v)
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
        for ax, obs, objects_list, title in zip(axes, [obse, obse2],
                                                [env.objects, env.objects_v],
                                                ["ram", "vision"]):
            for obj in objects_list:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
                # mark_point(obs, *opos[:2], color=(255, 255, 0))
            ax.imshow(obs)
            ax.set_title(title)
        for ax in axes.flatten():
            ax.set_xticks([])
            ax.set_yticks([])
        # plt.imshow(obse)
        # plt.show()
        plt.savefig(f"{SAVE_IMAGE_FOLDER}/{game_name}_{i}.png")
        print(f"Saved at {SAVE_IMAGE_FOLDER}/{game_name}_{i}.png for iou {stats['mean_iou']}")
        report_bad[f"Image_{i}"] = stats

    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()

ALL_STATS["mean_ious"] = np.mean(ALL_STATS["mean_ious"])
for class_name, value in ALL_STATS["per_class_ious"].items():
    ALL_STATS["per_class_ious"][class_name] = np.mean(value)
for only_in in ["only_in_ram", "only_in_vision"]:
    for obj_name, value in ALL_STATS[only_in].items():
        ALL_STATS[only_in][obj_name] = f"{value}/{NB_SAMPLES}"


json_report_bad = json.dumps(report_bad, indent=4)
json_report_bad = f"Details of frames with mean iou < {MIN_ACCEPTABLE_IOU}\n" + json_report_bad
with open(f"{SAVE_IMAGE_FOLDER}/report_bad_{game_name}.json", "w") as outfile:
    outfile.write(json_report_bad)
json_all_stats = json.dumps(ALL_STATS, indent=4)
with open(f"{SAVE_IMAGE_FOLDER}/all_stats_{game_name}.json", "w") as outfile:
    outfile.write(json_all_stats)
