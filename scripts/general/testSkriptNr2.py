import gymnasium as gym
import time
import random
# from matplotlib import pyplot as plt
"""
created by timo to set the ram and see whats changed
"""


env = gym.make("BeamRider", render_mode="human")
env.metadata['render_fps'] = 60
observation, info = env.reset(seed=42)
observation, reward, terminated, truncated, info = env.step(0)
ram = env.unwrapped.ale.getRAM()



for _ in range(1000):
    # env.unwrapped.ale.setRAM(105, 0)
    # action = policy(observation)  # User-defined policy function

    # -------------------manipulate ram----------------------------------
    
    target_ram_position = 25
    previous_ram_at_position = ram[target_ram_position]
    new_ram_value = 4
    # env.unwrapped.ale.setRAM(target_ram_position, new_ram_value)
    ram = env.unwrapped.ale.getRAM()

    # print(new_ram_value)
    # print(ram)
    if new_ram_value > 255 or new_ram_value < 0:
        print("ram out of bounds")
        new_ram_value = 0
    print(ram[target_ram_position])
    # env.unwrapped.ale.setRAM(11, 10)
    # -------------------------------------------------------------------
    terminated, truncated = False, False
    observation, reward, terminated, truncated, info = env.step(1)  # (random.randint(1,8))
    if terminated or truncated:
        observation, info = env.reset()

    rgb_array = env.render()
    """plt.imshow(rgb_array)  # rgb_array stuff for fun
    plt.show()
    print(rgb_array)"""

    time.sleep(0.01)
env.close()
