from ocatari.core import OCAtari

RENDER_MODE = "human"
# GAME = "ALE/MontezumaRevenge-v5"
# GAME = "ALE/Pong-v5"
# GAME = "ALE/Seaquest-v5"
# GAME = "ALE/Tennis-v5"
GAME = "ALE/Freeway-v5"

render_obs = True

if render_obs:
    import matplotlib.pyplot as plt

env = OCAtari(GAME, mode="ram",obs_mode="obj", hud=False, render_mode=RENDER_MODE,
             render_oc_overlay=True, frameskip=1)

env.reset()
i = 0
while True:
    action = env.action_space.sample()  # pick random action
    obs, _, _, done, _ = env.step(action)
    env.render()
    i = i+1 
    if render_obs and i % 100 == 0:
        plt.imshow(obs[0])  # For grayscale; remove `cmap` for color
        plt.colorbar()  # Optional: adds a color scale
        plt.show()
        import ipdb; ipdb.set_trace()
    if done:
        env.reset()
