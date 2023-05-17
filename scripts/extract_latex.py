import pandas as pd
import pickle

pkl_report_file = "reports/all_games_report.pkl"
latex_report_file = "reports/all_games_report.tex"
with open(pkl_report_file, "rb") as savefile:
    df = pickle.load(savefile)

import ipdb; ipdb.set_trace()

df = df[~df.index.duplicated(keep='first')]

# df.fillna("N/A", inplace=True)
dfT = df.T
dfT["mean"] = dfT.mean(axis=1)
df = dfT.T

df = df.round(1)


styler = df.style
styler.background_gradient(cmap="RdYlGn", vmin=0, vmax=100)
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
    "multicolumn{4}{c}{DQN}", "multicolumn{4}{c|}{DQN}")

with open(latex_report_file, 'w') as texfile:
    texfile.write(ltx_code)

print(f"Saved latex in {latex_report_file}")