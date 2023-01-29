from matplotlib import pyplot as plt

from ocatari.core import OCAtari
import time
import random
import ipdb


# env = OCAtari("Asterix-v4")
env = OCAtari("Asterix-v4", mode="vision", render_mode='rgb_array')  # Skiing-v4, DemonAttack-v4, SpaceInvaders-v4
observation, info = env.reset()
prevRam = None

# constant = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 19, 20, 21, 23, 24, 26, 27, 37, 38, 50, 51, 52, 53, 54, 55, 56, 57, 58,
# 59, 60, 61, 62, 63, 64, 65, 66, 67, 70, 72, 81, 82, 84, 85, 86, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
# 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 119, 120, 121, 122, 123,
# 124, 125, 126, 127]

constant = []
not_important = constant + []
already_figured_out = not_important + list(range(42, 50))  # 50 is excluded
                                            # x_lanes
value = 0
ctr = 0

for ROUND in range(1000000):

    print('round =', ROUND, 'ctr =', ctr)
    obs, reward, terminated, truncated, info = env.step(random.randint(-2, -1))

    if prevRam is not None:
        value = (prevRam[ctr] + 31) % 256

        if ROUND % 8 == 0:
            ctr = ctr + 1
        if ROUND > 1:
            env._env.unwrapped.ale.setRAM(ctr, value)

        print(ram)

        for i in range(len(ram)):
            if ram[i] != prevRam[i] and i not in already_figured_out or i == 26 or i == 16:
                integ = ram[i] - prevRam[i]

                if integ > 127:
                    print(str(i), '\t', -integ, '\t',
                          format(-integ, '08b'), '\t',
                          str(ram[i]), '\t',
                          format(ram[i], '08b'),
                          "negativ")
                else:
                    print(str(i), '\t', integ, '\t',
                          format(integ, '08b'), '\t',
                          str(ram[i]), '\t',
                          format(ram[i], '08b')
                          )
        if info.get('frame_number') > 150:
            if ROUND > 80:

                # if k % 3 == 0:  # round was k before
                #     wert = 2^(wert + 1)

                print("by index", value)
                '''for l in range(8):
                    wert = (prevRam[index] + 4) % 256
                    env._env.unwrapped.ale.setRAM(index, wert) '''

        print("------------------------------------------")
        # prevRam = ram
        if terminated or truncated:
            observation, info = env.reset()
        print(info)

        env.render()
        if info.get("frame_number") % 1 == 0:
            rgb_array = env.render()
            plt.imshow(rgb_array)  # rgb_array stuff for fun
            plt.show()
            print(rgb_array)
        time.sleep(0)
    if ROUND > 0:
        prevRam = ram
    ram = env._env.unwrapped.ale.getRAM()
env.close()
