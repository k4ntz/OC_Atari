import gymnasium as gym
import time
# created by timo to set the ram and see whats changed

env = gym.make("Seaquest", render_mode="human")
env.metadata['render_fps'] = 60
observation, info = env.reset(seed=42)
observation, reward, terminated, truncated, info = env.step(0)

for _ in range(1000):
    # action = policy(observation)  # User-defined policy function

    # -------------------manipulate ram----------------------------------
    ram = env.unwrapped.ale.getRAM()
    target_ram_position = 33
    previos_ram_at_position = ram[target_ram_position]
    new_ram_value = 225     # previos_ram_at_position+50#random.randint(0, 255)
    # print(new_ram_value)
    print(ram)
    if new_ram_value > 255 or new_ram_value < 0:
        print("ram out of bounds")
        new_ram_value = 0
    env.unwrapped.ale.setRAM(target_ram_position, new_ram_value)
    # -------------------------------------------------------------------
    terminated, truncated = False, False
    observation, reward, terminated, truncated, info = env.step(5)
    # env.render()
    if terminated or truncated:
        observation, info = env.reset()

    time.sleep(0.01)
env.close()
