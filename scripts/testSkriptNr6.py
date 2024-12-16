from matplotlib import pyplot as plt
from ocatari.core import OCAtari
import random

"""
this test makes it easy to test several indices individually or at once and to read the BITS of changing values
"""

env = OCAtari("SpaceInvaders-v4", mode="vision",
              render_mode='rgb_array')  # Skiing-v4, DemonAttack-v4
observation, info = env.reset()
prevRam = None

constant = []
not_important = constant  # + list(range(55, 57))
already_figured_out = not_important  # + list(range(94, 97)) \
# + list(range(41, 50))  # + list(range(19, 27)) + list(range(29, 37))

value = 1  # initial value you begin with
index = 54

for ROUND in range(10000000):

    obs, reward, terminated, truncated, info = env.step(random.randint(0, 2))

    if prevRam is not None:
        # i = 9  # to test an individual index in all rounds (so the index keeps constant)
        i = index  # here the index meant to be incremented

        # don't delete these lines
        # value = (prevRam[i] + 31) % 256  # 31 = 00001111
        # value = (prevRam[i] + 32) % 256  # 32 = 00010000
        # value = (prevRam[i] + 33) % 256  # 33 = 00010001 (in 15 rounds you changed every bit)
        # value = (prevRam[i] + 3) % 256
        # 85 = 01010101 for efficient changes (= more and fast) (2 rounds)
        value = (prevRam[i] + 85) % 256
        # value = (prevRam[i] + 1) % 256
        # value = (prevRam[i] + 16) % 256
        # value = (prevRam[i] * 2) % 256
        # const = 1
        # value = prevRam[i] + const * pow(-1, ROUND % 2)  # to alternate
        # if ROUND % 2 == 0:
        #     value = prevRam[i] -1
        # else:
        #     value = prevRam[i] + 1
        # value = -ram[i]  # here you invert all bits at once
        # value = 86
        # value = (prevRam[i] + 1) % 8
        # if ram[72] % 128>0:
        #     value = ram[72]
        # else:
        #     value = 128 + ram[72]

        if ROUND % 4 == 0:  # how often we increment index
            index += 1
            while index in already_figured_out:
                index += 1

        if ROUND % 1 == 0 and ROUND > 60:
            env._env.unwrapped.ale.setRAM(i, value)  # DON'T CHANGE
            for k in range(len(ram)):
                if ram[k] != prevRam[k] and k not in already_figured_out:
                    string = ""
                    if ram[k] >= prevRam[k]:
                        integer = ram[k] - prevRam[k]
                        string = "+" + str(integer)
                    else:
                        integer = prevRam[k] - ram[k]
                        string = "-" + str(integer)

                    print(str(k), '\t', string, '\t',
                          format(integer, '08b'), '\t',
                          str(ram[k]), '\t',
                          format(ram[k], '08b')
                          )

            env.render()
            rgb_array = env.render()
            plt.imshow(rgb_array)  # rgb_array stuff for fun
            plt.show()
            print(ram)
            print("------------------------------------------")

        if terminated or truncated:
            observation, info = env.reset()
        # print(info)

        if ROUND > 1:
            print('round =', ROUND, 'ram[' + str(i) + '] =', ram[i])
            # for k in [6, 38, 54, 83, 88, 89, 120]:  # checking set of specific values
            #     print('ram[' + str(k) + '] =', ram[k])
        else:
            print('round =', ROUND, 'i =', i)

        # time.sleep(0.1)
    if ROUND > 0:
        prevRam = ram
    ram = env._env.unwrapped.ale.getRAM()
env.close()
