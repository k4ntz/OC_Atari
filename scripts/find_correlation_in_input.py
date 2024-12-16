import sys
import matplotlib.pyplot as plt
from copy import deepcopy
from tqdm import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import RANSACRegressor, LinearRegression
sys.path.insert(0, '../ocatari')  # noqa
from ocatari.core import OCAtari
import pickle


DROP_LOW = True
MIN_CORRELATION = 0.6


def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=50, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10)
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()


print(f"Loading from {sys.argv[1]}")
ram_saves, target_values = pickle.load(open(sys.argv[1], 'rb'))

objects_infos = {"target": target_values}

ram_saves = np.array(ram_saves).T
from_rams = {str(i): ram_saves[i] for i in range(
    128) if not np.all(ram_saves[i] == ram_saves[i][0])}
objects_infos.update(from_rams)
df = pd.DataFrame(objects_infos)

# df["sum"] = df["Projectile_1_y"] + df["Projectile_2_y"]
# df["diff"] = df["Projectile_1_y"] - df["Projectile_2_y"]
# subset.append("sum")
# subset.append("diff")
# print(np.array(objects_infos['Projectile_1_y']) > np.array(objects_infos['Projectile_2_y']))

# find correlation
METHOD = "spearman"
# METHOD = "kendall"
METHOD = "pearson"
corr = df.corr(method=METHOD)
# Reduce the correlation matrix
subset = ["target"]
# [f"{obj}_x" for obj in object_list] + [f"{obj}_y" for obj in object_list]


# Use submatrice
corr = corr[subset].T
corr.drop(subset, axis=1, inplace=True)

if DROP_LOW:
    # corr = corr[corr.columns[[corr.abs().max() > MIN_CORRELATION]]]
    corr = corr.loc[:, (corr.abs() > MIN_CORRELATION).any()]

# if METHOD == "pearson":
ax = sns.heatmap(corr, vmin=-1, vmax=1, annot=True,
                 cmap=sns.diverging_palette(20, 220, n=200))
# else:
#     ax = sns.heatmap(corr, vmin=0, vmax=1, annot=True, cmap=sns.diverging_palette(20, 220, n=200))
# ax.set_yticklabels(ax.get_yticklabels(), rotation=90, horizontalalignment='right')


for tick in ax.get_yticklabels():
    tick.set_rotation(0)

xlabs = corr.columns.to_list()
plt.xticks(list(np.arange(0.5, len(xlabs) + .5, 1)), xlabs)
plt.title("Correlation")
plt.show()

# import ipdb;ipdb.set_trace()


corrT = corr.T
ser = corr.abs().max()
ser.sort_values(ascending=False)
for el in corrT:
    for idx, val in ser.sort_values(ascending=False).items():
        if val > 0.9:
            x, y = df[idx], df[el]
            # a, b = np.polyfit(x, y, deg=1)
            a, b = ransac_regression(x, y)
            plt.scatter(x, y, marker="x")
            plt.plot(x, a * x + b, color="k", lw=2.5)
            print(f"{el} = {a:.3f} x ram[{idx}] + {b:.3f} ")
            plt.xlabel(idx)
            plt.ylabel(el)
            plt.show()
