import gym
import time

# created by timo to print out the ram changes and general testing


'''
env = gym.make("Breakout", render_mode="human")
observation, info = env.reset(seed=42)

for _ in range(1000):
   #action = policy(observation)  # User-defined policy function
   observation, reward, terminated, truncated, info = env.step(1)

   if terminated or truncated:
      observation, info = env.reset()
env.close()


from ocatari import OCAtari
import time
env = OCAtari("BreakoutNoFrameskip-v4")
observation, info = env.reset(seed=42)
for i in range(1000):
    actionSpace = env._env.action_space
    action = actionSpace.sample()
    obs, reward,terminated, done, info = env.step(1)
    if terminated or done:
        observation, info = env.reset()
    #print(info)
    ram = env._env.env.unwrapped.ale.getRAM()
    print(ram)
    env.render()
    time.sleep(0.01)
env.close()
'''

env = gym.make("Skiing", render_mode="human")
observation, info = env.reset(seed=42)
prevRam = None
already_figured_out = [25, 107, 104, 105, 106, 14]  # all the ram positions you already know
filter = [0, 29, 98, 101] + already_figured_out  # additional filter
for _ in range(1000):
    # action = policy(observation)  # User-defined policy function
    observation, reward, terminated, truncated, info = env.step(0)

    ram = env.unwrapped.ale.getRAM()
    if prevRam is not None:
        for i in range(len(ram)):
            if ram[i] != prevRam[i] and i not in filter:
                pad = "           "
                for u in range(4 - len(str(i))):
                    pad += " "  # so unnötig xD
                print(str(i) + pad + "value:" + str(ram[i]))
    print("------------------------------------------")

    prevRam = ram
    '''rgb_array = env.render()
    plt.imshow(rgb_array)   #rgb_array stuff for fun
    plt.show()
    print(rgb_array)'''

    if terminated or truncated:
        observation, info = env.reset()

    time.sleep(0.01)
env.close()
