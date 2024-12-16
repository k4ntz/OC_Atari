import random
import time
from copy import deepcopy

import gymnasium as gym
import ipdb

from ocatari.utils import *
from ocatari.core import OCAtari
from matplotlib import pyplot as plt
from pynput import keyboard

from ocatari.vision.utils import make_darker, mark_bb


# running this file will start the game in multiple different ways given by the following variables:
# if True, running this file will execute the OCAtari code
useOCAtari = True
# if True, the extracted objects or the environment info will be printed
printEnvInfo = False

# OCAtari modes
mode = "vision"                    # ram, vision, test
mode = "ram"                    # ram, vision, test
HUD = True                      # if True, the returned objects are only the necessary ones

# gym[atari]/gymnasium
# game name, e.g.: ChopperCommand-v4, Pong, Boxing or ...
game_name = "ChopperCommand-v4"
# render_mode => "rgb_array" is advised, when playing
render_mode = "rgb_array"
# => "human" to also get the normal representation to compare between object extraction and default
seed = 42                       # resetting environment seed
fps = 30                        # render fps


# actions
# possible action inputs given by a run with showInputs = True
# number of actions that will be performed until the environment shuts down automatically
performActions = 30000
INPUTS = ['NOOP', 'FIRE', 'UP', 'RIGHT', 'LEFT', 'DOWN', 'UPRIGHT', 'UPLEFT', 'DOWNRIGHT', 'DOWNLEFT', 'UPFIRE',
          'RIGHTFIRE', 'LEFTFIRE', 'DOWNFIRE', 'UPRIGHTFIRE', 'UPLEFTFIRE', 'DOWNRIGHTFIRE', 'DOWNLEFTFIRE']
playGame = True                # if True, enables inputs if you want to play
key_map = {                     # the inputs mapped to the possible basic actions
    'f': 'FIRE',                    # -> every other action should be a combination of them
    'up': 'UP',
    'right': 'RIGHT',
    'left': 'LEFT',
    'down': 'DOWN'}
# the set of active basic actions (related to the currently pressed keys)
isActive = set()
# the default action if nothing is pressed or a false combination is pressed
default_action = 'NOOP'
actionSequence = []             # only used if playGame is False
# -> repeats the action sequence until the number of actions reaches performActions
# -> if no sequence is defined, it repeats random actions instead

# get valuable information for reversed engineering purposes and others
# if True, prints the number and the description of the possible inputs (actions)
showInputs = True
showActions = False             # if True, prints the action that will be done
showRAM = False                 # if True, prints the RAM to the console
showImage = True                # if True, plots the image
printRGB = False                # if True, prints the rgb array
slowDownPlot = 0.001            # pause per iteration
# RAM manipulation
manipulateRAM = False           # if True, you can set the RAM by an index
setRAMIndex = 72                # the index of the ram that will be set
# the value of the ram that will be set (if negative, then it counts up)
setRAMValue = 10
# shows any other changes that occurred by changing the ram (dependent on env.step)
showDelta = False
lastRAM = np.zeros(128)
ipdb_delay = 0                  # delay of ipdb interrupt and chance to use the plot

# DO NOT CHANGE! global variables used in context of the key control
pause = False                   # press tab to pause
end = False                     # press esc to end
ipdb_pause = False              # press i to interrupt with ipdb
interrupted = False


def with_gym():
    """
    Sets up the gym environment and runs the game
    """
    # set up environment
    env = gym.make(game_name, render_mode=render_mode)
    env.reset(seed=seed)
    env.metadata['render_fps'] = fps

    run(env)


def with_ocatari():
    """
    Sets up the gym environment wrapped into the OCAtari2.0 and runs the game
    """
    # set up environment
    oc = OCAtari(env_name=game_name, mode=mode,
                 hud=HUD, render_mode=render_mode)
    oc.reset(seed=seed)
    # oc.metadata['render_fps'] = fps, access to this would be nice ???

    run(oc)


def run(env):
    """
    runs the game in the given environment
    env: the environment
    """
    # key input handling
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    if playGame:
        # remove all inputs that are bound to plotting
        for x in key_map:
            for key in plt.rcParams:
                if key.startswith("keymap"):
                    li = plt.rcParams[key]
                    if x in li:
                        li.remove(x)

    # initialize stuff
    global pause, lastRAM
    manager = None
    delta = np.ndarray(shape=[128])

    # getThePossibleInputs
    number_of_actions = env.action_space.n
    actions = get_unwrapped(env).get_action_meanings()
    if showInputs:
        print(number_of_actions)
        print(actions)

    # display image
    if showImage:
        # activate interactive modus
        plt.ion()
        plt.show(block=False)

    # run the game
    for i in range(performActions):
        # get the action that will be performed
        if playGame:
            # based on user input
            action_name = get_action_name(isActive)
            action = actions.index(action_name)
        elif actionSequence is None or len(actionSequence) == 0:
            # randomly generated
            action = random.randint(0, number_of_actions - 1)
            action_name = actions[action]
        else:
            # given by the action sequence
            action_name = actionSequence[i % len(actionSequence)]
            action = actions.index(action_name)

        # print current action
        if showActions:
            print(action_name)

        # do a step with the given action
        observation, reward, terminated, truncated, info = env.step(action)
        # returns if the environment is in the terminal state (end) -> terminated, truncated
        if terminated or truncated:
            observation, info = env.reset()

        # print valuable information
        print_environment_info(env, observation, reward, info)

        # RAM
        ram = get_unwrapped(env).ale.getRAM()
        if showRAM:
            print(ram)

        # adjust the RAM as you like to see what it changes in the rendering (functional behavior of the RAM is
        # not important and therefore must not be part of the project, but the changes that are visually displayed)
        if useOCAtari and manipulateRAM:
            if setRAMValue < 0:
                # the expected value must not be negative, count up instead
                value = i % 256
            else:
                value = setRAMValue
                value %= 256
            env.set_ram(setRAMIndex, value)
            print("ram changed in (index, value):", setRAMIndex, value)
            ram = get_unwrapped(env).ale.getRAM()
            for j in range(len(ram)):
                delta[j] = ram[j] - lastRAM[j]
            if showDelta:
                # the frame is stored at 0 and not interesting
                for j in range(len(delta)):
                    if delta[j] != 0:
                        print("difference in (index, value) = ", j, delta[j])

            lastRAM = deepcopy(ram)

        # preparation for the image output
        if useOCAtari and not manipulateRAM:
            for obj in env.objects:
                x, y = obj.xy
                if x < 160 and y < 210:
                    object_position = obj.xywh
                    object_color = obj.rgb

                    # change rgb a tiny bit, so that it is distinguishable from the objects color
                    bb_color = make_darker(object_color)
                    r, g, b = bb_color
                    if r+g+b <= 20:
                        bb_color = 255, 255, 255
                    mark_bb(observation, object_position, color=bb_color)
            image = observation
        else:
            # RGB
            rgb_array = env.render()
            if printRGB:
                print("rgb_array: ")
                print(rgb_array)
            image = rgb_array

        # display image
        if showImage and image is not None:
            if manager is not None:
                manager.remove()  # remove the last plot to avoid stacking plots
            manager = plt.imshow(image)  # wrap the array as an image
            # pause the interaction for a bit, so that the plot is drawn
            plt.pause(0.001)
            plt.pause(slowDownPlot)

        # test usage of ipdb

        # if paused, then interrupt, but keep the plotting functions
        while pause:
            # take a look at the frame
            plt.pause(1)

            # ending must be possible
            if end:
                plt.close('all')
                break

        # ipdb interrupt
        global ipdb_pause
        if ipdb_pause:
            ipdb_interrupt(ipdb_delay)
            ipdb_pause = False

        # if escaped, end the program
        if end:
            plt.close('all')
            break

    # close the environment at the end
    env.close()
    listener.stop()


def get_unwrapped(env):
    """
    env: the environment
    unwraps the environment to gain access to the ram information or ale
    """
    if useOCAtari:
        return env._env.env.unwrapped
    else:
        return env.unwrapped


def print_environment_info(env, observation, reward, info):
    """
    prints the environment info if the printEnvInfo variable is set to True
    """

    if not printEnvInfo:
        return

    if useOCAtari:
        # Besides the extraction, ocatari gives back valuable information
        if mode == "raw":
            print("raw data:\n", info)
        elif mode == "ram":
            print("objects revised:\n", env.objects)
        elif mode == "vision":
            print("objects vision:\n", env.objects)
        elif mode == "both":
            print("objects revised:\n", env.objects)
            print("objects vision:\n", env.objects_v)
    else:
        print(info)


def ipdb_interrupt(plot_time=0):
    """
    If you want to take a look at something with ipdb, pls use this function!
    plot_time: describes how long the plot will be accessible, starting from the point in time, when
    ipdb interrupts the code flow. If it is 0, then you won't be able to use the plot figure, because
    it runs on the same thread as this. While the ipdb interrupt takes place, you can activate the access to
    the plot figure for another x seconds by typing in plt.pause(x).
    """

    # while ipdb interrupt takes place, the key listener shouldn't listen to anything
    global interrupted
    interrupted = True

    # pause the plot
    if plot_time != 0:
        plt.pause(plot_time)

    # ipdb interrupt
    ipdb.set_trace()

    # interruption ends
    interrupted = False


def on_press(key):
    """
    By pressing keys, you can play the game (given by the key_map), freeze a frame (pressing tab),
    end the program (pressing escape) or use ipdb (pressing i)!
    This function particularly only sets variables needed for that control, which are used in the primary function run!
    """
    # running thread while ipdb interrupt
    global pause, end, ipdb_pause

    if not interrupted:
        # pausing based on space
        if key == keyboard.Key.tab:
            pause = not pause

        # ending program based on escape
        if key == keyboard.Key.esc:
            end = True

        # other inputs
        key_name = str(key)
        if key_name.startswith("Key."):
            key_name = key_name[4:]
        if "\'" in key_name:
            key_name = key_name.replace("\'", "")
        # key_name = key_name.removeprefix("\'")
        # key_name = key_name.removesuffix("\'")

        # ipdb
        if key_name == 'i':
            ipdb_pause = True

        # game control given by the key_map => add inputs to the list of active keys
        if key_name in key_map.keys():
            input_action = key_map[key_name]
            isActive.add(input_action)
        # print(input_action)
        # print(pause)


def on_release(key):
    """
    Removes keys from the list of active keys, when key is released
    """
    if not interrupted:
        # changing inputs
        key_name = str(key)
        if key_name.startswith("Key."):
            key_name = key_name[4:]
        if "\'" in key_name:
            key_name = key_name.replace("\'", "")
        # key_name = key_name.removeprefix("Key.")
        # key_name = key_name.removeprefix("\'")
        # key_name = key_name.removesuffix("\'")

        if key_name in key_map.keys():
            # print("released")
            input_action = key_map[key_name]
            isActive.remove(input_action)


def get_action_name(my_set=None):
    """
    Gets the action name based on a set of actions that will be considered a combination
    """

    for action_name in INPUTS:
        length = 0
        number = 0
        # compute how many elements of the set are part of the action name
        for x in my_set:
            if -1 != action_name.find(x):
                # number of contained elements of the set increases
                number += 1
                # length of the combined string increases
                length += len(x)
            else:
                break
        # every element in the set must be contained
        # and there shouldn't be more parts of the name that are not in the set
        if number == len(my_set) and length == len(action_name):
            return action_name
    # if you haven't found anything, return the default action
    return default_action


if useOCAtari:
    with_ocatari()
else:
    with_gym()
