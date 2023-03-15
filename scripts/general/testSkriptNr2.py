import gymnasium as gym
import time
import random
# from matplotlib import pyplot as plt
"""
created by timo to set the ram and see whats changed
"""


env = gym.make("Qbert", render_mode="human")
env.metadata['render_fps'] = 60
observation, info = env.reset(seed=42)
observation, reward, terminated, truncated, info = env.step(2)

for i in range(1000):
    # action = policy(observation)  # User-defined policy function

    # -------------------manipulate ram----------------------------------
    ram = env.unwrapped.ale.getRAM()
    env.unwrapped.ale.setRAM(75, 1)
    target_ram_position = 76
    previous_ram_at_position = ram[target_ram_position]
    new_ram_value = 3
    env.unwrapped.ale.setRAM(target_ram_position, new_ram_value)
    env.unwrapped.ale.setRAM(77, 5)
    env.unwrapped.ale.setRAM(78, 7)
    env.unwrapped.ale.setRAM(79, 9)
    # print(ram[14], ram[15])
    # print(ram[41])
    # print(ram[target_ram_position])
    if new_ram_value > 255 or new_ram_value < 0:
        print("ram out of bounds")
        new_ram_value = 0
    # env.unwrapped.ale.setRAM(11, 10)
    # -------------------------------------------------------------------
    terminated, truncated = False, False
    if i < 100:
        observation, reward, terminated, truncated, info = env.step(3)
    else:
        observation, reward, terminated, truncated, info = env.step(0)
    if terminated or truncated:
        observation, info = env.reset()

    rgb_array = env.render()
    """plt.imshow(rgb_array)  # rgb_array stuff for fun
    plt.show()
    print(rgb_array)"""

    time.sleep(0.01)
env.close()
