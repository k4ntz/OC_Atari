import time
import random
import ipdb
from matplotlib import pyplot as plt
import sys
import os
import numpy as np
# import pathlib
sys.path.insert(0, '../../')  # noqa

from ocatari.core import OCAtari

"""
set the ram and see whats changed
"""

env_id = "Breakout"
obs_mode = "obj"
seed = 42
frameskip = 1

# Seeding
os.environ['PYTHONHASHSEED'] = str(seed)
# torch.use_deterministic_algorithms(args.torch_deterministic)
# torch.backends.cudnn.deterministic = args.torch_deterministic
# torch.backends.cudnn.benchmark = False
# torch.cuda.manual_seed_all(args.seed)
random.seed(seed)
np.random.seed(seed)

env = OCAtari(env_id, hud=False, render_mode="rgb_array", mode="ram",
              render_oc_overlay=False, obs_mode=obs_mode, frameskip=1)


env.action_space.seed(seed)

observation, info = env.reset(seed=seed)
observation, reward, terminated, truncated, info = env.step(0)


for _ in range(100):
    action = env.action_space.sample()  # pick random action
    obs, reward, truncated, terminated, info = env.step(action)

obs1 = obs
print("---")

env = OCAtari(env_id, hud=False, render_mode="rgb_array", mode="vision",
              render_oc_overlay=False, obs_mode=obs_mode, frameskip=1)

env.action_space.seed(seed)

observation, info = env.reset(seed=seed)
observation, reward, terminated, truncated, info = env.step(0)


for _ in range(100):
    action = env.action_space.sample()  # pick random action
    obs, reward, truncated, terminated, info = env.step(action)

obs2 = obs

if obs_mode == "dqn":
    obs2 = obs2[0]
    obs1 = obs1[0]

# Compute the difference
difference = np.abs(obs1 - obs2)

# Plot the difference as a grayscale image

fig, axes = plt.subplots(1, 3, figsize=(10, 5))

axes[0].imshow(obs1, cmap="gray")
axes[0].set_title("OBS1")

axes[1].imshow(obs2, cmap="gray")
axes[1].set_title("OBS2 Visualization")

axes[2].imshow(difference, cmap="gray")
axes[2].set_title("Difference Visualization")

plt.tight_layout()
plt.show()


env.close()
