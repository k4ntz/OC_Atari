import gymnasium as gym
import time
# import matplotlib.pyplot as plt
import ipdb

"""
print out a ram that always has values within range
"""

env = gym.make("MsPacman", render_mode="human")
observation, info = env.reset(seed=42)
prevRam = None
min = 0
max = 2
candidates = []
counterMax = 100
counter = 0
already_figured_out = [70, 97, 102, 30, 31, 32, 33,
                       62, 59, 57, 58, 103, 102] + list(range(71, 75))
for _ in range(1000):
    ipdb.set_trace()
    # action = policy(observation)  # User-defined policy function
    observation, reward, terminated, truncated, info = env.step(0)
    ram = env.unwrapped.ale.getRAM()
    print(ram)
    # ------------------------------------manage candidates-------------------
    if counter <= 0:
        counter = counterMax
        print("-----added new candidates-----")
        for i in range(len(ram)):
            if max > 255 or (ram[i] >= min and ram[i] <= max):
                if i not in already_figured_out:
                    candidates.append(i)
    else:
        throwaways = []
        if max > 255:  # range not specified so throw out evrything that changes
            for i in candidates:
                if prevRam[i] != ram[i]:
                    throwaways.append(i)
        else:
            for i in candidates:
                if ram[i] > max or ram[i] < min:
                    throwaways.append(i)
        # remove all throwaways
        for t in throwaways:
            candidates.remove(t)

    # -------------------------print out candidates-------------------------------
    for i in candidates:
        print(str(i) + ":   " + str(ram[i]))
    print("------------------------------------------")

    prevRam = ram

    if terminated or truncated:
        observation, info = env.reset()

    time.sleep(0.01)
env.close()
