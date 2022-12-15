from ocatari import OCAtari
import time
import random
import ipdb
""""
test Atari games with the ipdb debugger to see the RAM changes for each consecutive frame
"""
env = OCAtari("Breakout")
observation, info = env.reset()
prevRam = None
already_figured_out = []
for i in range(1000):
    if info.get('frame_number') > 20:
        ipdb.set_trace()

    obs, reward, terminated, truncated, info = env.step(random.randint(0, 0))
    ram = env._env.unwrapped.ale.getRAM()
    if prevRam is not None:
        for i in range(len(ram)):
            if ram[i] != prevRam[i] and i not in already_figured_out:
                pad = "           "
                for u in range(4 - len(str(i))):
                    pad += " "
                print(str(i) + pad + "value:" + str(ram[i]) + pad + " was previously " + str(prevRam[i]))
    print("------------------------------------------")
    prevRam = ram

    if terminated or truncated:
        observation, info = env.reset()
    print(info)
    env.render()
    time.sleep(0.01)
env.close()
