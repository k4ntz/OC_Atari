from matplotlib import pyplot as plt

from ocatari.core import OCAtari
import time
import random

# this test makes it easy to test several indices

env = OCAtari("Asterix-v4", mode="vision", render_mode='rgb_array')  # Skiing-v4, DemonAttack-v4, SpaceInvaders-v4
observation, info = env.reset()
prevRam = None

constant = []
not_important = constant + []
already_figured_out = not_important + list(range(41, 50)) + list(range(94, 97))\
                      + list(range(29, 37)) + list(range(19, 27))

value = 0
index = 61
for ROUND in range(1000000):

    # if ROUND > 0:
    #     print('round =', ROUND, 'ram[' + str(index-1) + '] =', ram[index-1])
        # for k in [6, 38, 54, 83, 88, 89, 120]:  # checking specific values
        #     print( 'ram[' + str(k) + '] =', ram[k])
    # else:
    #     print('round =', ROUND, 'index =', index)
    obs, reward, terminated, truncated, info = env.step(random.randint(-2, 2))

    if prevRam is not None:
        i = 39  # to test an individual index in all rounds (where the index keeps constant)
        # i = index  # here the index meant to be incremented

        # value = (prevRam[i] + 31) % 256  # 31 = 00011111
        # value = (prevRam[i] + 3) % 256
        # value = (prevRam[i] + 51) % 256  # 51 = 00110011 for efficient changes (= more and fast)
        # value = (prevRam[i] + 1) % 256
        # value = (prevRam[i] + 16) % 256
        # value = (prevRam[i] * 2) % 256
        # value = prevRam[i] + ( -1 ^ ( ROUND % 2 ))
        # if ROUND % 2 == 0:
        #     value = prevRam[i] -1
        # else:
        #     value = prevRam[i] + 1
        # value = -ram[i]
        # value = 86

        if ROUND % 3 == 0:
            while index in already_figured_out:
                index = index + 1
            index = index + 1

        # if ROUND > 1:
        #     env._env.unwrapped.ale.setRAM(i, value)  # DON'T CHANGE. CHANGE ABOVE

        # print(ram)

        env._env.unwrapped.ale.setRAM(83, 2)
        # env._env.unwrapped.ale.setRAM(94, 10)
        # env._env.unwrapped.ale.setRAM(95, 10)

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

        print("------------------------------------------")

        if terminated or truncated:
            observation, info = env.reset()
        # print(info)

        env.render()
        if ROUND % 100 == 1:
            env._env.unwrapped.ale.setRAM(96, ram[96]+10)
            env._env.unwrapped.ale.setRAM(95, ram[95] + 10)
        if ROUND % 100 == 0:
            rgb_array = env.render()
            plt.imshow(rgb_array)  # rgb_array stuff for fun
            plt.show()
        time.sleep(0)
    if ROUND > 0:
        prevRam = ram
    ram = env._env.unwrapped.ale.getRAM()
env.close()
