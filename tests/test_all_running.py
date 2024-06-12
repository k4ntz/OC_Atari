from ocatari.core import OCAtari, AVAILABLE_GAMES
from metrics_utils import *
from tqdm import tqdm
import sys, inspect
import random

NB_SAMPLES = 100
ONLYBOTHDEFINEDOBJECTS = True

normal_stdout = sys.stdout
devnull = open('/dev/null', 'w')



for game in AVAILABLE_GAMES:
    # if game < "V":
    #     continue
    if ONLYBOTHDEFINEDOBJECTS:
        classes = []
        for mode in ["ram", "vision"]:
            mod_path = f"ocatari.{mode}.{game.lower()}"
            classes.append([el[0] for el in inspect.getmembers(sys.modules[mod_path], inspect.isclass)])
        classes_in_both = set.intersection(set(classes[0]) & set(classes[1]))
    try:
        env = OCAtari(game, mode="both", render_mode='rgb_array', hud=True)
    except:
        env = OCAtari(f"ALE/{game}-v5", mode="both", render_mode='rgb_array', hud=True)
    det_scores = DetectionScores()
    env.reset()
    # sys.stdout = devnull
    print(f"Testing {game}:")
    for step in tqdm(range(10*NB_SAMPLES)):
        action = env.action_space.sample()
        obse, reward, terminated, truncated, info = env.step(action)
        if random.random() < 0.1:
            robjects = env.objects
            vobjects = env.objects_v
            stats = get_all_metrics(robjects, vobjects)
            det_scores.update(stats["dets"])
    print(det_scores)
