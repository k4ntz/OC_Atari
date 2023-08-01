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
from detect_walls import detect_Walls

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
file_name = "walls_configurations.txt"
file_path = os.path.join(current_directory, file_name)
code_file = open(file_path, "a")
code = ""
# snapshot = pickle.load(open("kangstarted.pkl", "rb"))
# env._env.env.env.ale.restoreState(snapshot)


level_ram = 117
config_ram = 28
code += "def add_walls_to_object_list(ram_state, objects, objects_map):\n"
for level_number in range(0, 20):
    indentation = "    "
    if level_number == 0:
        code += indentation + f"if ram_state[117] == {level_number}:\n"
    else:
        code += indentation + f"elif ram_state[117] == {level_number}:\n"
    env.set_ram(level_ram, level_number)
    for i in range(30):
        env.step(0)
    env.set_ram(32, 0)
    env.set_ram(43, 81)
    for configuration_number in range(number_of_configuration_per_level[level_number]):
        indentation = "    "
        # destroy destructible walls
        env.set_ram(32, 0)
        indentation += "    "
        if configuration_number == 0:
            code += indentation + f"if ram_state[28] == {configuration_number}:\n"
        else:
            code += indentation + f"elif ram_state[28] == {configuration_number}:\n"
        # env._env.env.env.ale.restoreState(snapshot)
        env.set_ram(config_ram, configuration_number)
        resulting_obs, _, _, _, _ = env.step(0)
        env.set_ram(31, 60)
        if configuration_number == number_of_configuration_per_level[level_number] - 1:
            env.set_ram(27, env.get_ram()[41])
            for i in range(30):
                env.step(1)
        print(f"level {level_number} configuration number {configuration_number}")

        walls = detect_Walls(resulting_obs)
        indentation += "    "
        # show_ims(resulting_obs, level_number, configuration_number)
        for i in range(len(walls)):
            wall = walls[i]
            code += indentation + "wall_instance = Wall()\n"
            code += indentation + f"wall_instance.xy = {wall.xy}\n"
            code += indentation + f"wall_instance.wh = {wall.wh}\n"
            code += indentation + "objects.append(wall_instance)\n"
            code += indentation + f"objects_map['fixed_wall {i}'] = wall_instance\n"
        code += indentation + f"number_of_walls = {len(walls)}\n"
        code += indentation + "i = 0\n"
        code += indentation + """while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):\n"""
        indentation += "    "
        code += indentation + """objects_map.pop(f"fixed wall {number_of_walls + i}")\n"""
        code += indentation + "i += 1\n"

    code += "\n"
code += "    " + "return objects, objects_map"
code_file.write(code)
code_file.close()
