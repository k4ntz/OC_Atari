from ocatari.core import OCAtari

RENDER_MODE = "human"
GAME = "ALE/Seaquest-v5"

env = OCAtari(GAME, mode="revised", hud=True, render_mode=RENDER_MODE, render_oc_overlay=True)
env.reset()

while True:
    action = env.action_space.sample()  # pick random action
    done = env.step(action)[3]
    env.render()
    if done:
        env.reset()
