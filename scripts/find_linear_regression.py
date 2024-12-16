"""
Demo script that allows me to find the linear relation between selected ram states and
detected objects through vision in game
"""
import pathlib
import pickle
# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
from copy import deepcopy
from math import ceil

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from tqdm import tqdm

sys.path.insert(0, '../ocatari')  # noqa
from ocatari.core import OCAtari
from ocatari.utils import load_agent, parser, make_deterministic

# IMPORTANT: sets the actions of the player during the acquisition of the data.
actions = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4] + [0] * 400
# Coefficients below this value will be ignored.
SIGNIFICANCE_THRESHOLD = 0.1

parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-to", "--tracked_object", type=str, default=["Player"], nargs=1,
                    help="A list of objects to track")
parser.add_argument("-tp", "--tracked_property", type=str, default=['x'], nargs=1,
                    help="A list of properties to track for each object")
parser.add_argument("-tr", "--tracked_rams", type=int, nargs='+',
                    help="A list of the ram emplacements to use for the linear regression \n"
                         "Note: Can put the same ram emplacement twice and elevate it to different degrees")
parser.add_argument("-d", "--degrees", type=int, nargs='*',
                    help="The degree to elevate each of the ram values used in the ")
parser.add_argument("-tn", "--top_n", type=int, default=3,
                    help="The top n value to be kept in the correlation matrix")
parser.add_argument("-ns", "--nb_samples", type=int, default=1000,
                    help="The number of samples to use.")
parser.add_argument("-dqn", "--dqn", action="store_true", help="Use DQN agent")
parser.add_argument("-s", "--seed", default=0,
                    help="Seed to make everything deterministic")
parser.add_argument("-r", "--render", action="store_true",
                    help="If provided, renders")
parser.add_argument("-m", "--method", type=str, default="pearson", choices={"pearson", "spearman", "kendall"},
                    help="The method to use for computing the correlation")
parser.add_argument("-snap", "--snapshot", type=str, default=None,
                    help="Path to an emulator state snapshot to start from.")
opts = parser.parse_args()

if opts.degrees is None:
    opts.degrees = [1] * len(opts.tracked_rams)
else:
    if len(opts.tracked_rams) != len(opts.degrees):
        raise ValueError(
            'The degrees list must have the same length as the number of rams value to take into account')

MODE = "vision"
if opts.render:
    RENDER_MODE = "human"
else:
    RENDER_MODE = "rgb_array"
env = OCAtari(opts.game, mode=MODE, render_mode=RENDER_MODE)

make_deterministic(opts.seed, env)

observation, info = env.reset()
if opts.snapshot:
    snapshot = pickle.load(open(opts.snapshot, "rb"))
    env._env.env.env.ale.restoreState(snapshot)

tracked_property_values = []

if opts.dqn:
    opts.game = opts.game
    opts.path = f"models/{opts.game}/dqn.gz"
    try:
        dqn_agent = load_agent(opts, env.action_space.n)
    except FileNotFoundError:
        oc_atari_dir = pathlib.Path(__file__).parents[1].resolve()
        opts.path = str(oc_atari_dir / 'models' / f"{opts.game}" / 'dqn.gz')
        dqn_agent = load_agent(opts, env.action_space.n)

ram_saves = []
for i in tqdm(range(opts.nb_samples)):
    # Here to change the actions of the player
    # prob = random.random()
    # if prob > 0.9:
    #     action = 2 # UP
    # elif prob > 0.8:
    #     action = 5 # DOWN
    # else:
    #     action = 4 # 4-RIGHT 3- Left, Truck at (56, 129), (16, 18), Cactus at (125, 55), (8, 8), Cactus at (129, 46), (8, 8)]
    # if i % 5: # reset for pressing
    #     action = 0
    action = 0
    if opts.dqn:
        action = dqn_agent.draw_action(env.dqn_obs)
    else:
        action = actions[i % len(actions)]
    obs, reward, terminated, truncated, info = env.step(action)

    if info.get('frame_number') > 10 and i % 1 == 0:
        SKIP = False
        for obj_name in opts.tracked_object:  # avoid state without the tracked objects or with several
            if str(env.objects).count(f"{obj_name} at") != 1:
                SKIP = True
                break
        if SKIP:
            continue
        for obj in env.objects:
            objname = obj.category
            if objname == opts.tracked_object[0]:
                prop = opts.tracked_property[0]
                # A modified property can also be used by replacing what is appended to the list.
                # For example for a string having w**2 + h**2 can give norm or maybe track a count or an angle
                # calculated using the division of x/y of an object. Example we know the center the rope is in (78,34):
                # tracked_property_values.append((obj.xy[0] - 78) ** 2 + (obj.xy[1] - 34) ** 2))
                tracked_property_values.append(obj.__getattribute__(prop))
        ram = env._env.unwrapped.ale.getRAM()
        ram_saves.append(deepcopy(ram))
        if terminated or truncated:
            observation, info = env.reset()
            if opts.snapshot:
                env._env.env.env.ale.restoreState(snapshot)

env.close()

if len(ram_saves) == 0:
    print("No data point was taken")

ram_saves = np.array(ram_saves).T
from_rams = {str(i): ram_saves[i] for i in range(
    128) if not np.all(ram_saves[i] == ram_saves[i][0])}
X = []
y = tracked_property_values
unchanged_rams = []
for j in range(len(opts.tracked_rams)):
    ram = int(opts.tracked_rams[j])
    degree = int(opts.degrees[j])
    # Same here if special transformations are needed depending on the value of the ram --> for example
    # if the ram_saves[98] == 128 must multiply by -1 the value of ram[94] then in the try loop can be put:
    # if ram == 94:
    #     if ram_saves[98] == 128:
    #       X.append(list(map(lambda x:pow(-x, degree), from_rams[str(ram)][i]**degree)))
    #     else:
    #       X.append(list(map(lambda x:pow(-x, degree), from_rams[str(ram)][i]**degree)))
    try:
        X.append(list(map(lambda x: pow(x, degree), from_rams[str(ram)])))
    except KeyError:
        print(
            f"the ram located at the emplace number {ram} doesn't change during the duration of the acquisition.")
        unchanged_rams.append(ram)

# Fitting of the model
try:
    X = np.array(X).T
    reg = LinearRegression().fit(X, np.array(y))
except ValueError:
    raise ValueError(
        "Only ram emplacements with unchanged values throughout the acquisition were given.")

coeffs = reg.coef_
coeffs[np.abs(coeffs) < SIGNIFICANCE_THRESHOLD] = 0
coeffs = np.round(coeffs, decimals=ceil(abs(np.log10(SIGNIFICANCE_THRESHOLD))))
approximate_reg = LinearRegression()
approximate_reg.intercept_ = reg.intercept_ if abs(
    reg.intercept_) > SIGNIFICANCE_THRESHOLD else 0
approximate_reg.coef_ = coeffs

# Display the result
print("score = " + str(approximate_reg.score(X, y)))
coeffs = coeffs.tolist()
final_expression = f"{reg.intercept_} + " if approximate_reg.intercept_ != 0 else ""
for i in range(len(opts.tracked_rams)):
    if opts.tracked_rams[i] not in unchanged_rams and coeffs[i] != 0:
        if i != len(opts.tracked_rams) - 1:
            final_expression += f"{coeffs[i]} * (ram_state[{opts.tracked_rams[i]}]"
            final_expression += f"**{opts.degrees[i]}) +" if opts.degrees[i] != 1 else ") +"
        else:
            final_expression += f"{coeffs[i]} * (ram_state[{opts.tracked_rams[i]}]"
            final_expression += f"**{opts.degrees[i]})" if opts.degrees[i] != 1 else ")"
plt.title(final_expression)
plt.scatter(X[:, coeffs.index(max(coeffs))], y)
plt.plot(X[:, coeffs.index(max(coeffs))], approximate_reg.predict(X))
plt.xlabel(opts.tracked_rams[j])
plt.ylabel(opts.tracked_object[0] + opts.tracked_property[0])
plt.show()
print(final_expression)
