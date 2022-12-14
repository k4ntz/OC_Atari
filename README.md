# OC_Atari

Object-Centric Atari is a Wrapper, based on the [ATARI ARI project](https://github.com/mila-iqia/atari-representation-learning) that uses the state of the ram and reverse engineering to provide object centric representation of the screen.


## List of covered games

### Priority 1:
- [ ]  Breakout (missing revised, vision)
- [x]  Freeway
- [ ]  Bowling (worked on by Chris)
- [ ]  Ms.  Pacman (worked on by Bjarne)
- [x]  Pong
- [ ]  Seaquest (rework revised, vision)
- [ ]  Skiing (rework revised, vision)
- [ ]  Space Invaders (worked on by Belal/Sebastian)
- [ ]  Asterix
- [ ]  Asteroids
- [ ]  Demon Attack
- [x]  Tennis
- [ ]  Kangaroo

### Priority 2:
- [ ]  Berzerk
- [ ]  Secret Quest
- [ ]  River Raid
- [ ]  Atlantis
- [ ]  Star Raiders
- [ ]  Choppper Command
- [ ]  Q*bert
- [ ]  Assault
- [ ]  Beam Rider
- [ ]  Boxing
- [ ]  Carnival
- [ ]  Centipede

### Priority 3:
- [ ]  Montezumas Revenge
- [ ]  Private Eye
- [ ]  Fishing Derby
- [ ]  Zaxxon
- [ ]  Wizard of Wor

### Priority 4:
- [ ]  Crazy Climber
- [ ]  Video Pinball
- [ ]  Alien

## Install
`python setup.py install` or `python setup.py develop`


## Usage
Test the `demo_pong.py` script
You can change the `mode` argument line 10!


##
```py
from ocatari import OCAtari
import time
import random
env = OCAtari("Skiing")
observation, info = env.reset()
for i in range(1000):
   #action = self._action_set[1]

   #done split into 2 parts:
   #terminated = True if env terminates (completion or failure),
   # truncated = True if episodes truncates due to a time limit or a reason that is not defined of the task
    obs, reward, terminated, truncated, info = env.step(random.randint(0, 2))
    if terminated or truncated:
        observation, info = env.reset()
    print(info)
    env.render()
    time.sleep(0.01)
env.close()
```

## Downloading trained atari agents
For trained agents, I use agents of [this repo](https://github.com/floringogianu/atari-agents)

### Use these trained agents:
Here is an example:
`python3.8 demo_pong.py -p models/Tennis/1/model_50000000.gz`
