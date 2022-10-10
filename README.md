# OC_Atari


Object-Centric Atari is a Wrapper, based on the [ATARI ARI project](https://github.com/mila-iqia/atari-representation-learning) that uses the state of the ram and reverse engineering to provide object centric representation of the screen.

##
```py
from ocatari import OCAtari
env = OCAtari("BreakoutNoFrameskip-v4")
for i in range(1000):
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    print(info)
    env.render()
    time.sleep(0.01)
env.close()
```
