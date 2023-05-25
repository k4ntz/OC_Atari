import pandas as pd
import pickle
from termcolor import colored

pkl_report_file = "reports/all_games_report.pkl"
latex_report_file = "reports/all_games_report.tex"
with open(pkl_report_file, "rb") as savefile:
    df = pickle.load(savefile)


df = df[~df.index.duplicated(keep='last')]

nb_games = len(df)
print(colored(f"{nb_games} out of 35 done !"))

# df.fillna("N/A", inplace=True)
dfT = df.T
dfT["mean"] = dfT.mean(axis=1)
df = dfT.T

df = df.round(1)


styler = df.style
styler.background_gradient(cmap='Spectral', vmin=0, vmax=100)
styler.format(precision=1, na_rep="N/A")
styler.highlight_null("gray")
ltx_code = styler.to_latex(
    caption=f"Statistiques on all games",
    clines="skip-last;data",
    convert_css=True,
    position_float="centering",
    hrules=True,
    multicol_align="c"
)

ltx_code = ltx_code.replace("100.0", "100").replace("\n & 0 \\\\\n\\midrule", "")
ltx_code = ltx_code.replace("lrrrrrrrrrrr", "l|rrrr|rrrr|rrrr").replace(
        "multicolumn{4}{c}{Random}", "multicolumn{4}{c|}{Random}").replace(
    "multicolumn{4}{c}{DQN}", "multicolumn{4}{c|}{DQN}").replace("mean", "\\bottomrule\nmean")

with open(latex_report_file, 'w') as texfile:
    texfile.write(ltx_code)



print(f"Saved latex in {latex_report_file}")