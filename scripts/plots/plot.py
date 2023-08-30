import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from pathlib import Path
import numpy as np
import os
import matplotlib.ticker as mticker
from matplotlib import rc

rc('text', usetex=True)


sns.set()

def form(x):
    # if x == 0.1:
    #     return '0.1'
    # else:
    #     return str(int(x))
    return str(10*int(x))


# take every X sample for plot (raw log interval: 20k frames) default: 6
DATA_PLOT_SPARSITY = 100

# rolling average sample window (applied after sparsity) default: 4
DATA_PLOT_SMOOTHNESS = 4

MAX_TRAINING_STEPS = 20000000

# in and out dirs
logs_dir = Path.cwd() / Path("logs")
out_dir = Path.cwd() / Path("plots")

# envs to look for in logdir and subdirs and plot
envs = ["Asterix", "Tennis", "Pong", "Boxing", "Freeway"]

# experiments to exclude from plots:
dont_plot = []

# scalars to look for in tfevent files and plot
scalar_to_plot = {
    "tb_name" : "rollout/ep_rew_mean",
    "xlabel": "Frames (M)",
    "ylabel": "Human Normalized Return (\%)"}

# human baseline data per env
human_baselines = {
    "Pong" : 14.6,
    "Boxing" : 12.10,
    "Freeway" : 29.6, 
    "Asterix" : 8503.3,
    "Tennis" : -8.3
}

# random baseline data per env
random_baselines = {
    "Pong" : -20.7,
    "Boxing" : 0.10,
    "Freeway" : 0.00,
    "Asterix" : 210.0,
    "Tennis" : -23.8
}

data = pd.read_csv("out.csv", index_col=0)
data.value *= 100 # percent
data = data.loc[data['step'] <= 10.1]
# data = pickle.load(open("out.pkl", "rb"))


# games = ["Asterix"]

# def extract_game_info(data):
#     all_values = []
#     all_seeds = []
#     for seed in [0, 8, 16]:
#         dgs = data_game[data_game["seed"] == seed]
#         print(dgs[:70])

# for game in games:
#     data_game = data[data["curve_id"] == game]
#     extract_game_info(data_game)


fig_size = (6, 3.8)
fig = plt.figure(figsize=fig_size)


order = sorted(data["curve_id"].unique())
ax = plt.gca()
p5, = ax.plot([0], marker='None', linestyle='None', label=r"\textbf{OC}")
ax = sns.lineplot(data=data, x="step", y="value", hue="curve_id", hue_order=order, ax=ax)
p5, = ax.plot([0],  marker='None', linestyle='None', label=r"\textbf{Deep}")
deep_vals = {}
for game, col in zip(order, sns.color_palette()):
    values = []
    if not os.path.exists(f"{game.lower()}"):
        continue
    for seed in range(3):
        path = f"{game.lower()}/run-{seed}/eval/mean_reward.csv"
        csvdt = pd.read_csv(path)
        values.append(csvdt)
    steps, mvals = np.mean(values, axis=0).T
    _, svals = np.std(values, axis=0).T
    rnd = random_baselines[game]
    hmn = human_baselines[game]
    mvals = 100*(mvals-rnd) / (hmn-rnd) 
    svals = 100*(svals-rnd) / (hmn-rnd)
    # steps /= 1000000
    steps = np.linspace(0., 10., 50)
    ax.plot(steps, mvals, '--', color=col, label=game)
    ax.fill_between(steps, mvals-svals, mvals+svals, color=col, alpha=0.1)


ax.set_facecolor('white')
ax.grid(color='#e0e0e0', linestyle='-', linewidth=1)
ax.set(
    xlabel = scalar_to_plot["xlabel"],
    ylabel = scalar_to_plot["ylabel"])
# print(ax.get_xlim())
ax.set_xlim(-0.3, 10.2)

# plt.plot(np.zeros(1), np.zeros([1,3]), color='w', alpha=0, label=' ')
# plt.plot(np.zeros(1), np.zeros([1,3]), color='w', alpha=0, label=' ')

ax.axhline(100, ls="dashdot", color="grey")
plt.yscale("log")
ax.set_xticklabels([f'{int(x)}' for x in ax.get_xticks()])
ax.set_yticklabels([f'{form(x)}' for x in ax.get_yticks()])
# ax.set_yticklabels([f'{100*int(x)}' for x in ax.get_yticks()])
# ax.set_ylim(bottom=0)
# plt.subplots_adjust(top = 0.9, bottom=0.15, left=0, right=1)

ax.legend(loc='lower right', fontsize=12, ncols=2)


ax.spines['bottom'].set_color('0.5')
ax.spines['top'].set_color('0.5')
ax.spines['right'].set_color('0.5')
ax.spines['left'].set_color('0.5')
ax.set_ylim(0.5, 540)

plt.tight_layout()
plt.savefig("graph.svg")
plt.show()


# plt.plot(x, mean_1, 'b-', label='mean_1')
# plt.fill_between(x, mean_1 - std_1, mean_1 + std_1, color='b', alpha=0.2)
# plt.plot(x, mean_2, 'r--', label='mean_2')
# plt.fill_between(x, mean_2 - std_2, mean_2 + std_2, color='r', alpha=0.2)

# plt.legend(title='title')
# plt.show()