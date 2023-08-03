"""
Demo script that allows me to find the correlation between ram states and
detected objects through vision in Tennis
"""

import os
import random
import sys
from copy import deepcopy

import matplotlib.pyplot as plt

sys.path.insert(0, '../ocatari')  # noqa
from ocatari.core import OCAtari
# from alive_progress import alive_bar
from ocatari.utils import parser, make_deterministic
from ocatari.vision.utils import find_objects
from ocatari.vision.hero import Lamp
from ocatari.vision.hero import Platform

number_of_configuration_per_level = [2, 4, 6, 8, 8, 10, 12, 14, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]

parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")

opts = parser.parse_args()

MODE = "vision"
RENDER_MODE = "human"
RENDER_MODE = "rgb_array"
env = OCAtari(opts.game + "NoFrameskip", mode=MODE, render_mode=RENDER_MODE)
random.seed(0)

make_deterministic(0, env)

get_bin = lambda x: format(int(x), 'b').zfill(8)

observation, info = env.reset()

base_next_obs, _, _, _, _ = env.step(0)
base_objects = deepcopy(env.objects)
binary_mode = False


def show_ims(obs, level_number, configuration_number):
    plt.imshow(obs)
    plt.title(f"level set to {level_number} and configuration {configuration_number})", fontsize=20)
    plt.show()


snapshot = None
current_directory = os.path.dirname(os.path.abspath(__file__))
file_name = "enemy_types.txt"
file_path = os.path.join(current_directory, file_name)
code_file = open(file_path, "a")
code = ""
# snapshot = pickle.load(open("kangstarted.pkl", "rb"))
# env._env.env.env.ale.restoreState(snapshot)

Y_MIN_GAMEZONE = 20
Y_MAX_GAMEZONE = 138
X_MIN_GAMEZONE = 8
X_MAX_GAMEZONE = 142


def detect_lamp_and_plateform(obs):
    lamps_and_platforms = []
    for lamp in find_objects(obs, [142,142,142], miny=Y_MIN_GAMEZONE, maxy=Y_MAX_GAMEZONE,
                             minx=X_MIN_GAMEZONE):
        lamp = Lamp(*lamp)
        if lamp.h < 10 and lamp.h > 2:
            lamps_and_platforms.append(lamp)
    for platform in find_objects(obs, [232, 232, 74], miny=Y_MIN_GAMEZONE, maxy=Y_MAX_GAMEZONE,
                                 minx=X_MIN_GAMEZONE):
        platform = Platform(*platform)
        if platform.w > 6:
            lamps_and_platforms.append(platform)
    return lamps_and_platforms


level_ram = 117
config_ram = 28

lamps_first_part_of_stage = []
lamps_second_part_of_stage = []
lamps_third_part_of_stage = []
platforms_presence = []
for level_number in range(0, 20):
    env.set_ram(level_ram, level_number)
    for i in range(30):
        env.step(0)
    env.set_ram(43, 81)
    for configuration_number in range(number_of_configuration_per_level[level_number]):
        env.set_ram(config_ram, configuration_number)
        env.set_ram(31, 60)
        if configuration_number == number_of_configuration_per_level[level_number] - 1:
            env.set_ram(27, env.get_ram()[41])
            for i in range(30):
                env.step(1)
        print(f"level {level_number} configuration number {configuration_number}")
        resulting_obs, _, _, _, _ = env.step(0)

        for i in range(4):
            env.set_ram(32+i, 0)

        lamps_and_platforms = detect_lamp_and_plateform(resulting_obs)
        print(lamps_and_platforms)
        stage_zone_y = [60, 100, 150]
        for i in range(len(lamps_and_platforms)):
            lamp_or_platform = lamps_and_platforms[i]
            if isinstance(lamp_or_platform, Lamp):
                if lamp_or_platform.y < stage_zone_y[0]:
                    lamps_first_part_of_stage.append((level_number, configuration_number))
                elif lamp_or_platform.y < stage_zone_y[1]:
                    lamps_second_part_of_stage.append((level_number, configuration_number))
                else:
                    lamps_third_part_of_stage.append((level_number, configuration_number))
            else:
                platforms_presence.append((level_number, configuration_number))

print("lamps_first_part_of_stage = ", lamps_first_part_of_stage)
print("lamps_second_part_of_stage = ", lamps_second_part_of_stage)
print("lamps_third_part_of_stage = ", lamps_third_part_of_stage)
print("platforms_presence = ", platforms_presence)
code_file.write(code)
code_file.close()
