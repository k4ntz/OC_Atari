from matplotlib.transforms import ScaledTranslation
import json
import matplotlib.pyplot as plt
import numpy as np
# import seaborn as sns

# sns.set_style("whitegrid")

speed_dict = json.load(open('speedtests.json'))

reduction = {
    'ChopperCommand': 'ChopperC.',
    'MontezumaRevenge': 'Montezum.',
    'SpaceInvaders': 'SpaceInv.',
}

fig = plt.gcf()
ax = plt.gca()
fig.set_size_inches(10, 5)
plt.grid()
ax.set_axisbelow(True)

games = list(speed_dict.keys())
print(games)
ram_perfs = [speed_dict[g]['ram'] if 'ram' in speed_dict[g] else []
             for g in games]
vision_perfs = [speed_dict[g]['vision']
                if 'vision' in speed_dict[g] else [] for g in games]


width = 0.26
offsets = [-width/2, width/2]
xs = np.arange(len(games))
for perfs, of, lab, col in zip([ram_perfs, vision_perfs], offsets, ['RAM', 'Vision'], ['C0', '#ED6246']):
    means = [np.average(times) for times in perfs]
    stds = [np.std(times) for times in perfs]
    plt.bar(xs+of, means, width, yerr=stds, label=lab, color=col)
    print(lab, np.mean(means))

for i, game in enumerate(games):
    if game in reduction:
        games[i] = reduction[game]

plt.yscale('log')
plt.xticks(xs, games, rotation=70, fontsize=14)
ax.tick_params(axis='y', which='major', labelsize=14)
dx, dy = -5, 3
offset = ScaledTranslation(dx / fig.dpi, dy / fig.dpi, fig.dpi_scale_trans)
for label in ax.xaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset)

plt.xlim(-0.5, len(games)-0.5)
plt.ylabel("Execution Time (log scale)", fontsize=16)
plt.xlabel("Game", fontsize=16)
plt.legend(loc="upper right", fontsize=14, ncol=2)


plt.tight_layout()

plt.savefig("speedtest.svg")
plt.show()
