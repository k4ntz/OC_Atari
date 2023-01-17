# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import random
import matplotlib.pyplot as plt
from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.tennis import objects_colors
# from ocatari.vision.pong import objects_colors
from ocatari.utils import load_agent, test_parser
from copy import deepcopy
import numpy as np
import os


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
    detailled_ious = {}
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
                    if objname not in detailled_ious:
                        detailled_ious[objname] = [iou]
                    else:
                        detailled_ious[objname].append(iou)
                    vobj._is_in_ram = True
                    robj._is_in_image = True
                    break
    for robj in ram_list:
        if not robj._is_in_image:
            only_in_vision.append(robj)
    for vobj in vision_list:
        if not vobj._is_in_ram:
            only_in_vision.append(vobj)
    return np.mean(ious), detailled_ious, only_in_ram, only_in_vision

SAVE_IMAGE_FOLDER = "diff_images"
os.makedirs(SAVE_IMAGE_FOLDER, exist_ok=True)
opts = test_parser.parse_args()
game_name = opts.game
MODE = "test"
HUD=True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()


if opts.path:
    agent = load_agent(opts, env.action_space.n)


fig, axes = plt.subplots(1, 2)
for i in range(10000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, 5)
    obse, reward, terminated, truncated, info = env.step(action)
    avg_iou, d_ious, oir, oiv = difference_objects(env.objects, env.objects_v)
    if avg_iou < 0.5:
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
        # plt.show()
        plt.savefig(f"{SAVE_IMAGE_FOLDER}/{game_name}_{i}.png")
        print(f"Saved at {SAVE_IMAGE_FOLDER}/{game_name}_{i}.png for iou {avg_iou}")



    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
