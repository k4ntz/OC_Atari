from ocatari.core import OCAtari

RENDER_MODE = "human"
GAME = "ALE/Seaquest-v5"

env = OCAtari(GAME, mode="revised", hud=True, render_mode=RENDER_MODE, render_oc_overlay=True)
env.reset()

while True:
    env.step(env.action_space.sample())  # act randomly
    env.render()
