"""
Demo script that allows to find the correlation between ram states and
detected objects through vision in a specified game.
"""

# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
from copy import deepcopy
from tqdm import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import RANSACRegressor, LinearRegression
from os import path
import pathlib
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from ocatari.core import OCAtari
from ocatari.utils import parser, load_agent, make_deterministic
import pickle
from time import sleep


def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=15, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10)
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()



parser.add_argument("-tn", "--top_n", type=int, default=0,
                         help="The top n value to be kept in the correlation matrix")
parser.add_argument("-ns", "--nb_samples", type=int, default=1000,
                         help="The number of samples to use.")
parser.add_argument("-d", "--data", type=str, required=True, help="Path to the data file")
parser.add_argument("-m", "--method", type=str, default="pearson", choices={"pearson", "spearman", "kendall"},
                    help="The method to use for computing the correlation")
opts = parser.parse_args()


ACTIONS, RAMS = pickle.load(open(opts.data, "rb"))


ram_saves = np.concatenate((np.expand_dims(np.array(ACTIONS), 1), np.array(RAMS)), axis=1)

ram_saves = np.array(ram_saves).T
from_rams = {str(i-1): ram_saves[i] for i in range(128) if not np.all(ram_saves[i] == ram_saves[i][0])}
from_rams["actions"] = from_rams.pop("-1")
df = pd.DataFrame(from_rams)

import ipdb; ipdb.set_trace()
# find correlation
corr = df.corr(method=opts.method)
# Reduce the correlation matrix
# [f"{obj}_x" for obj in opts.tracked_objects] + [f"{obj}_y" for obj in opts.tracked_objects]
print("-"*20)
for el, onlynans in corr.isna().all(axis=1).items():
    if onlynans:
        print(f"Only NaNs found for {el} in the correlation matrix, most probably fix attribute.")
print("-"*20)
# Use submatrice
# corr = corr[subset].T
# corr.drop(subset, axis=1, inplace=True)

if opts.top_n:
    print(f"Filtering, keeping only top {opts.top_n} correlated elements")
    # corr = corr[corr.columns[[corr.abs().max() > MIN_CORRELATION]]]
    to_keep = []
    for index, row in corr.iterrows():
        au_corr = row.to_frame().abs().unstack().sort_values(ascending=False)
        au_corr = au_corr[0:opts.top_n].dropna()
        to_keep.extend([key[1] for key in au_corr.keys() if key[1] not in to_keep])
    corr = corr[to_keep]


# if opts.method == "pearson":
ax = sns.heatmap(corr, vmin=-1, vmax=1, annot=True, cmap=sns.diverging_palette(20, 220, n=200))
# else:
#     ax = sns.heatmap(corr, vmin=0, vmax=1, annot=True, cmap=sns.diverging_palette(20, 220, n=200))
# ax.set_yticklabels(ax.get_yticklabels(), rotation=90, horizontalalignment='right')


for tick in ax.get_yticklabels():
    tick.set_rotation(0)

xlabs = corr.columns.to_list()
plt.xticks(list(np.arange(0.5, len(xlabs) + .5, 1)), xlabs)
plt.show()


print("-"*20)
print("Finding relashionshinps using RANSAC regression")
corrT = corr.T
for el in corrT:
    keys = corrT[el].keys()
    for idx in range(len(keys)):
        maxval = corrT[el].abs()[keys[idx]]
        #idx = corrT[el].abs()
        if maxval >= 0.6:
            x, y = df[keys[idx]], df[el]
            xys = pd.DataFrame({'x': x, 'y': y})
            # a, b = np.polyfit(x, y, deg=1)
            a, b = ransac_regression(x, y)
            for (xp, yp), sp in xys.value_counts(normalize=True).items():
                plt.scatter(xp, yp, marker="x", color="b", s=500*sp)
            if b >= 0:
                formulae = f"{el} = {a:.2f} * ram_state[{keys[idx]}] + {b:.2f} "
            else:
                formulae = f"{el} = {a:.2f} * ram_state[{keys[idx]}] - {-b:.2f} "
            print(formulae)
            plt.plot(x, a * x + b, color="k", lw=2.5, alpha=0.3)
            plt.title(formulae)
            plt.xlabel(keys[idx])
            plt.ylabel(el)
            plt.show()
