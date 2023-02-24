import gymnasium as gym
import time
from matplotlib import pyplot as plt

"""
created by timo to print out the ram changes and general testing
"""


env = gym.make("MsPacman", render_mode="human")
observation, info = env.reset(seed=42)
prevRam = None
# already_figured_out = [25, 107, 104, 105, 106, 14]  # all the ram positions you already know
# filter = [0, 29, 98, 101] + already_figured_out  # additional filter
for _ in range(1000):
    observation, reward, terminated, truncated, info = env.step(0)

    ram = env.unwrapped.ale.getRAM()
    if prevRam is not None:
        for i in range(len(ram)):
            if ram[i] != prevRam[i] and i not in filter:
                pad = "           "
                for u in range(4 - len(str(i))):
                    pad += " "
                print(str(i) + pad + "value:" + str(ram[i]))
    print("------------------------------------------")

    prevRam = ram

    rgb_array = env.render()
    plt.imshow(rgb_array)   #rgb_array stuff for fun
    plt.show()
    print(rgb_array)

    if terminated or truncated:
        observation, info = env.reset()

    time.sleep(0.01)
env.close()
