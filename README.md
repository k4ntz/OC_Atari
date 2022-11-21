# OC_Atari


Object-Centric Atari is a Wrapper, based on the [ATARI ARI project](https://github.com/mila-iqia/atari-representation-learning) that uses the state of the ram and reverse engineering to provide object centric representation of the screen.

##
```py
from OC_Atari.ocatari import OCAtari
import time
import random
env = OCAtari("Skiing")
observation, info = env.reset()
for i in range(1000):
   #action = self._action_set[1]

   #done split into 2 parts: 
   #terminated = True if env terminates (completion or failure), truncated = True if episodes truncates due to a time limit or a reason that is not defined of the task
    obs, reward, terminated, truncated, info = env.step(random.randint(0, 2))
    if terminated or truncated:
        observation, info = env.reset()
    print(info)
    env.render()
    time.sleep(0.01)
env.close()
```
