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
import pickle

# running this file will start the game in multiple different ways given by the following variables:

default_help = 'F  : FIRE\nTAB:PAUSE'
HELP_TEXT = plt.text(0, -10.2, default_help, fontsize=20)


useOCAtari = True                # if True, running this file will execute the OCAtari code
printEnvInfo = False             # if True, the extracted objects or the environment info will be printed

# gym[atari]/gymnasium
game_name = "FishingDerby-v4"    # game name ChopperCommand-v4
render_mode = "rgb_array"           # render_mode => "rgb_array" is advised, when playing
# => "human" to also get the normal representation to compare between object extraction and default
fps = 60                        # render fps
seed = 0

# actions
# possible action inputs given by a run with showInputs = True
INPUTS = ['NOOP', 'FIRE', 'UP', 'RIGHT', 'LEFT', 'DOWN', 'UPRIGHT', 'UPLEFT', 'DOWNRIGHT', 'DOWNLEFT', 'UPFIRE',
          'RIGHTFIRE', 'LEFTFIRE', 'DOWNFIRE', 'UPRIGHTFIRE', 'UPLEFTFIRE', 'DOWNRIGHTFIRE', 'DOWNLEFTFIRE']
performActions = 30000         # number of actions that will be performed until the environment shuts down automatically
playGame = True                 # if True, enables inputs if you want to play
key_map = {                     # the inputs mapped to the possible basic actions
'f': 'FIRE',                    # -> every other action should be a combination of them
'up': 'UP',
'right': 'RIGHT',
'left': 'LEFT',
'down': 'DOWN'}
isActive = set()                # the set of active basic actions (related to the currently pressed keys)
default_action = 'NOOP'         # the default action if nothing is pressed or a false combination is pressed
actionSequence = ['NOOP']  # only used if playGame is False
# -> repeats the action sequence until the number of actions reaches performActions
# -> if no sequence is defined, it repeats random actions instead


# OCAtari modes
mode = "ram"                    # ram, vision, test
HUD = True                      # if True, the returned objects contain only the necessary information to play the game

# get valuable information for reversed engineering purposes
showInputs = False              # if True, prints the number and the description of the possible inputs (actions)
showActions = False             # if True, prints the action that will be done
showRAM = False                 # if True, prints the RAM to the console
# render_mode=="rgb_array" only
printRGB = False                # if True, prints the rgb array
showImage = True                # if True, plots the rgb array

# RAM manipulation
manipulateRAM = False          # if True, you can set the RAM by an index
setRAMIndex = 52                 # the index of the ram that will be set
setRAMValue = 255                # the value of the ram that will be set (if negative, then it counts up)
showDelta = False               # shows any other changes that occured by changing the ram (dependent on env.step)
slowDownPlot = 0.0001              # pause per iteration
lastRAM = np.zeros(128)

# DO NOT CHANGE! global variables used in context of interrupting, but keeping the plot stable (must be False)
pause = False
end = False
interrupted = False

fig = plt.gcf()
fig.set_size_inches(10.5, 18.5)

SAVE_EVERY = 10
all_rams = []
target_vals = []
target_val = 0  # initial value
env = None

def withgym():
    """
    Sets up the gym environment and runs the game
    """
    # set up environment
    global env
    env = gym.make(game_name, render_mode=render_mode)
    env.reset(seed=seed)
    env.metadata['render_fps'] = fps

    run(env)


def withocatari():
    """
    Sets up the gym environment wrapped into the OCAtari2.0 and runs the game
    """
    # set up environment
    global env
    oc = OCAtari(env_name=game_name, mode=mode, hud=HUD, render_mode=render_mode)
    oc.reset(seed=seed)
    # oc.metadata['render_fps'] = fps, access to this would be nice ???
    env = oc
    snapshot = pickle.load(open("lvl3.pkl", "rb"))
    # env._env.env.env.ale.restoreState(snapshot)

    run(oc)


def distance_to_joey(player):
    max_dist = 344
    if player.y > 130:
        return 1 - (120 * 3 - player.x)/max_dist
    elif player.y > 70:
        return 1 - (120 + player.x)/max_dist
    elif player.y > 25:
        return 1 - (140 - player.x)/max_dist 
    else:
        return 1


# def repeat_upsample(rgb_array, k=4, l=4, err=[]):
#     # repeat kinda crashes if k/l are zero
#     if rgb_array is None:
#         raise ValueError("The rgb_array is None, probably mushroom_rl bug")
#     if k <= 0 or l <= 0:
#         if not err:
#             print("Number of repeats must be larger than 0, k: {}, l: {}, returning default array!".format(k, l))
#             err.append('logged')
#         return rgb_array
#     return np.repeat(np.repeat(rgb_array, k, axis=0), l, axis=1)


def run(env):
    # key input handling
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    global pause, lastRAM
    if playGame:
        # remove all inputs that are bound to plotting
        for x in key_map:
            # print(plt.rcParams.items())
            for key in plt.rcParams:
                # e.g. "keymap.enter"
                if key.startswith("keymap"):
                    li = plt.rcParams[key]
                    if x in li:
                        li.remove(x)

    # initialize
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
        plt.ion()  # activate interactive modus
        plt.show(block=False)

    # run the game
    previous_lives = 3
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

        if showActions:
            print(action_name)
            # print(action)

        # do a step with the given action
        observation, reward, terminated, truncated, info = env.step(action)
        # if info["lives"] < previous_lives:
        #     reward -= 10
        # previous_lives = info["lives"]
        # print(reward)
        player = env.objects[0]
        print(distance_to_joey(player))
        # returns if the environment is in the terminal state (end) -> terminated, truncated
        if terminated or truncated:
            observation, info = env.reset()

        printEnvironmentInfo(env, observation, reward, info)

        # RAM
        ram = get_unwrapped(env).ale.getRAM()
        if not i % SAVE_EVERY:
            all_rams.append(deepcopy(ram))
            target_vals.append(target_val)
        if showRAM:
            print(ram)

        # adjust the RAM as you like to see what it changes in the rendering (functional behavior of the RAM is
        # not important and therefore must not be part of the project, but the changes that are visually displayed)

        if manipulateRAM:
            if setRAMValue < 0:
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
                for j in range(1, len(delta)):
                    if delta[j] != 0:
                        print("difference in (index, value) = ", j, delta[j])

            lastRAM = deepcopy(ram)

            """
            # rendering dependant on the frame
            frame = ram[0]
            if frame == 255:
                env.set_ram(1, ram[1] + 1)
                frame = 0
            env.set_ram(0, frame + 1)
            image = env.render()
            if manager is not None:
                manager.remove()  # remove the last plot to avoid stacking plots
            manager = plt.imshow(image)  # wrap the array as an image
            """

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
            # import ipdb; ipdb.set_trace()
            manager = plt.imshow(image)  # wrap the array as an image
            plt.pause(0.001)  # pause the interaction for a bit, so that the plot is drawn
            plt.pause(slowDownPlot)

        # test usage of ipdb
        # ipdb_Interrupt(10)

        # if paused, then interrupt, but keep the plotting functions
        value = -1
        while pause:
            # take a look at the frame
            HELP_TEXT.set_text("space: enter new value\nTab  : Unpause")
            plt.pause(1)
            # print("is paused")

            if end:
                plt.close('all')
                break
        HELP_TEXT.set_text(default_help)
        # if escaped, end the program
        if end:
            plt.close('all')
            break

        #if manipulateRAM:
         #   plt.pause(1)
          #  env.set_ram(div, old_value)

    # close the environment at the end
    env.close()
    listener.stop()
    save_fn = "mode_change_kangaroo.pkl"
    pickle.dump((all_rams, target_vals), open(save_fn, "wb"))
    print(f"Saved in {save_fn}")


def get_unwrapped(env):
    if useOCAtari:
        return env._env.env.unwrapped
    else:
        return env.unwrapped


def printEnvironmentInfo(env, observation, reward, info):
    if not printEnvInfo:
        return
    if useOCAtari:
        # Besonderheit von ocatari ist neben der Extraktion, die in step() zwischengeschaltet ist, auch die Ausgabe
        # dieser Extrahierten Daten:
        # raw daten stehen in info (bekommt man durch oc.step(action))

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


def ipdb_Interrupt(plot_time=0):
    """
    if you want to take a look at something with ipdb, pls use this function
    the plot_time describes how long the plot will be accessible between the 2 ipdb interrupts
    if it is 0, then there will only be 1 interrupt
    """
    # note that only this thread is interrupted
    # note that the plot won't work while ipdb interrupts the program
    # the event loop is interrupted, so you have to activate it by plt.pause()
    # that's why you need to write plt.pause(10) in the ipdb console to activate the interaction for 10 seconds
    # if you know in advance how long you want it to plot, use this function with not 0

    global interrupted

    interrupted = True
    ipdb.set_trace()
    if plot_time != 0:
        plt.pause(plot_time)
        ipdb.set_trace()
    interrupted = False


def on_press(key):
    # running thread while ipdb interrupt
    global pause, end, listener, HELPTEXT, target_val

    if not interrupted:
        #print(key)
        # pausing based on space
        if key == keyboard.Key.tab:
            pause = not pause

        # ending program based on escape
        if key == keyboard.Key.esc:
            end = True
        
        global env
        if pause and key == keyboard.Key.space:
            ram_pos = int(input('please enter ram pos'))
            print(f"Currently as : {env.get_ram()[ram_pos]}")
            new_val = int(input('please enter new target value'))
            env.set_ram(ram_pos, new_val)

        # changing inputs
        key_name = str(key)
        key_name = key_name.removeprefix("Key.")
        key_name = key_name.removeprefix("\'")
        key_name = key_name.removesuffix("\'")
        if pause and key_name.lower() == "s":
            snapshot = env._env.env.env.ale.cloneState()
            filename = input('give_filename')
            pickle.dump(snapshot, open(filename, "wb"))
            print(f"Saved state under {filename}")

        if key_name in key_map.keys():
            input_action = key_map[key_name]
            isActive.add(input_action)
        # print(input_action)
        # print(pause)

def on_release(key):
    # changing inputs
    key_name = str(key)
    key_name = key_name.removeprefix("Key.")
    key_name = key_name.removeprefix("\'")
    key_name = key_name.removesuffix("\'")

    if key_name in key_map.keys():
        # print("released")
        input_action = key_map[key_name]
        isActive.remove(input_action)


#hiermit muss man danach nur noch prüfen, mit welchem set das set der aktiven inputs übereinstimmt
def getInput():
    #combine inputs
    values = key_map.values()
    mySet = set()
    dic = dict()
    for part in INPUTS:
        #aus dem String ein Set von Strings (wie values) machen
        s = part
        for value in values:
            sArr = s.split(value)
            if len(sArr)==1:
                #entweder nur value drin oder value nicht drin
                if sArr[0] == value:
                    #wenn nur der value drin ist, dann hinzufügen und dic updaten
                    mySet.add(value)
                    dic.update({mySet:part})
                    break
                else:
                    #value ist nicht drin, also weitermachen
                    continue
            else:
                # ein Teil ist value, der andere ist ein Rest, den man noch betrachten will
                if sArr[0]==value:
                    s = sArr[1]               # Rest, den man noch betrachten will
                else:
                    s = sArr[0]
                mySet.add(value)              # abgespaltener value wird hinzugefügt
    #am ende hat man ein dictionary von Set, String
    # wobei das set kombiniert den String ergibt
    return dic


def get_action_name(my_set=None):
    """
    Gets the action name based on a set of combined actions
    """
    #man könnte auch jedes mal schauen, ob jedes Element im Set ein Teil des INPUTS-Elements ist
    for action_name in INPUTS:
        #muss jedes x enthalten sein
        length = 0
        number = 0
        for x in my_set:
            if -1 != action_name.find(x):
                number += 1
                length += len(x)
            else:
                break
        # das set muss jeden Anteil enthalten
        # jedes element in myset muss in action_name enthalten sein
        # und action_name darf nur aus myset elementen bestehen
        if number == len(my_set) and length == len(action_name):
            return action_name
    # hat man nichts gefunden, so muss man auf den default zurückgreifen
    return default_action


if useOCAtari:
    withocatari()
else:
    withgym()
