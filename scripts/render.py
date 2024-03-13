from ocatari.core import OCAtari

RENDER_MODE = "human"
# GAME = "ALE/MontezumaRevenge-v5"
# GAME = "ALE/Pong-v5"
GAME = "ALE/Seaquest-v5"
# GAME = "ALE/Tennis-v5"
# GAME = "ALE/Freeway-v5"

env = OCAtari(GAME, mode="ram", hud=True, render_mode=RENDER_MODE,
              render_oc_overlay=True, frameskip=1)
env.reset()

while True:
    action = env.action_space.sample()  # pick random action
    done = env.step(action)[3]
    env.render()
    if done:
        env.reset()
