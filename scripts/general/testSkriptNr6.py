from matplotlib import pyplot as plt
from ocatari.core import OCAtari
import time
import random

"""
this test makes it easy to test several indices
"""

env = OCAtari("Asterix-v4", mode="vision", render_mode='rgb_array')  # Skiing-v4, DemonAttack-v4, SpaceInvaders-v4
observation, info = env.reset()
prevRam = None

constant = []
not_important = constant + list(range(55, 57))
already_figured_out = not_important + list(range(94, 97)) \
                      + list(range(41, 50))  # + list(range(19, 27)) + list(range(29, 37))


value = 128
index = 54

for ROUND in range(10000000):

    obs, reward, terminated, truncated, info = env.step(random.randint(-2, 2))

    if prevRam is not None:
        i = 54  # to test an individual index in all rounds (where the index keeps constant)
        # i = index  # here the index meant to be incremented

        # if ROUND > 1:
        #     env._env.unwrapped.ale.setRAM(i, value)  # DON'T CHANGE. CHANGE ABOVE

        # value = (prevRam[i] + 31) % 256  # 31 = 00001111
        # value = (prevRam[i] + 32) % 256  # 32 = 00010000
        # value = (prevRam[i] + 33) % 256  # 33 = 00010001
        # value = (prevRam[i] + 3) % 256
        # value = (prevRam[i] + 85) % 256  # 85 = 01010101 for efficient changes (= more and fast)
        # value = (prevRam[i] + 1) % 256
        # value = (prevRam[i] + 16) % 256
        # value = (prevRam[i] * 2) % 256
        # value = prevRam[i] + ( -1 ^ ( ROUND % 2 ))  # to alternate
        # if ROUND % 2 == 0:
        #     value = prevRam[i] -1
        # else:
        #     value = prevRam[i] + 1
        # value = -ram[i]
        # value = 86

        if ROUND % 3 == 0:
            index += 1
            while index in already_figured_out:
                index += 1

        # if ram[29] % 2 != 1:
        #     env._env.unwrapped.ale.setRAM(29, ram[29]+1)

        if ROUND > 1:
            env._env.unwrapped.ale.setRAM(i, value)  # DON'T CHANGE. CHANGE ABOVE

        env._env.unwrapped.ale.setRAM(83, 2)

        if ROUND % 40 == 0:
            print(ram)
            for k in range(len(ram)):
                if ram[k] != prevRam[k] and k not in already_figured_out:
                    if ram[k] > prevRam[k]:
                        integ = ram[k] - prevRam[k]
                    else:
                        integ = prevRam[k] - ram[k]

                    if integ > 127:
                        print(str(k), '\t', -integ, '\t',
                              format(-integ, '08b'), '\t',
                              str(ram[k]), '\t',
                              format(ram[k], '08b'),
                              "negativ")
                    else:
                        print(str(k), '\t', integ, '\t',
                              format(integ, '08b'), '\t',
                              str(ram[k]), '\t',
                              format(ram[k], '08b')
                              )

            env.render()
            rgb_array = env.render()
            plt.imshow(rgb_array)  # rgb_array stuff for fun
            plt.show()
            print("------------------------------------------")

        if terminated or truncated:
            observation, info = env.reset()
        # print(info)

        if ROUND > 1:
            print('round =', ROUND, 'ram[' + str(i) + '] =', ram[i])
            # for k in [6, 38, 54, 83, 88, 89, 120]:  # checking specific values
            #     print('ram[' + str(k) + '] =', ram[k])
        else:
            print('round =', ROUND, 'i =', i)

        # time.sleep(0)
    if ROUND > 0:
        prevRam = ram
    ram = env._env.unwrapped.ale.getRAM()
env.close()
