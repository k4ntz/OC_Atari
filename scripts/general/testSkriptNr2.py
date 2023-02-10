import gymnasium as gym
import time
import random
# from matplotlib import pyplot as plt
"""
created by timo to set the ram and see whats changed
"""


env = gym.make("Atlantis", render_mode="human")
env.metadata['render_fps'] = 60
observation, info = env.reset(seed=42)
observation, reward, terminated, truncated, info = env.step(3)

for _ in range(1000):
    # action = policy(observation)  # User-defined policy function
    target_ram_position = 23
    new_ram_value = 0
    # env.unwrapped.ale.setRAM(target_ram_position, new_ram_value)
    # env.unwrapped.ale.setRAM(48, 7)

    # -------------------manipulate ram----------------------------------
    ram = env.unwrapped.ale.getRAM()
    previous_ram_at_position = ram[target_ram_position]
    # print(new_ram_value)
    # print(ram)
    print(ram[target_ram_position])
    if new_ram_value > 255 or new_ram_value < 0:
        print("ram out of bounds")
        new_ram_value = 0
    # env.unwrapped.ale.setRAM(11, 10)
    # -------------------------------------------------------------------
    terminated, truncated = False, False
    observation, reward, terminated, truncated, info = env.step(3)
    if terminated or truncated:
        observation, info = env.reset()

    rgb_array = env.render()
    """plt.imshow(rgb_array)  # rgb_array stuff for fun
    plt.show()
    print(rgb_array)"""

    time.sleep(0.01)
env.close()
