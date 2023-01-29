from ocatari.core import OCAtari
import time
import random
import ipdb


env = OCAtari("Asterix-v4")
observation, info = env.reset()
prevRam = None

constant = [109]
not_important = constant + []
already_figured_out = not_important + []

wert = 0
ctr = 0

for k in range(1000000):

    print('k =', k, 'ctr =', ctr)
    obs, reward, terminated, truncated, info = env.step(random.randint(-2, -1))

    if prevRam is not None:
        wert = (prevRam[16] + 32) % 256

        if k % 2 == 0:
            ctr = ctr + 1
        if k > 75:
            env._env.unwrapped.ale.setRAM(16, wert)

        print(ram)

        # print("hier1;", literal_eval(str(hex(21))))

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
            if k > 80:

                '''if k % 3 == 0:
                    wert = 2^(wert + 1)'''

                print("by value", wert)
                '''for l in range(8):
                    wert = (prevRam[value] + 4) % 256
                    env._env.unwrapped.ale.setRAM(value, wert) '''

        print("------------------------------------------")
        # prevRam = ram
        if terminated or truncated:
            observation, info = env.reset()
        print(info)
        env.render()
        time.sleep(0)
    if k > 0:
        prevRam = ram
    ram = env._env.unwrapped.ale.getRAM()
env.close()
