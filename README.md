# Object-Centric Atari

---
Quentin Delfosse, Jannis Blüml, Bjarne Gregori, Sebastian Sztwiertnia, ...

Inspired by thw work of Anand et. al., we present OCAtari, an improved, extended and object-centric version of their [ATARI ARI project](https://github.com/mila-iqia/atari-representation-learning). 
The [Arcade Learning Environment](https://github.com/mgbellemare/Arcade-Learning-Environment) allows us to read the RAM state at any time of a game. 
This repository is a wrapper for the well known [Gynmasium project](https://github.com/Farama-Foundation/Gymnasium) , that uses the state of the ram and reverse engineering 
to provide object centric representation of the screen. It provides code for benchmarking, testing and generating object-centric representations of states.

* [Install](#install) -- Install all relevant dependencies and start using OCAtari yourself
* [Usage](#usage) -- Learn about the different environments OCAtari supports and enables
* [Producing your own dataset](#producing-your-own-dataset) -- OCAtari also support the generation of object-centric datasets for supported Atari games
* [Models and additional Information](#models-and-additional-information) -- Everything you need to know to reproduce our results

--- 

## List of covered games
- [ ] Alien (only vision)
- [X] Assault
- [X] Asterix
- [ ] Asteroids  (only vision)
- [X] Atlantis
- [ ] BeamRider  (only vision)
- [X] Berzerk
- [X] Bowling
- [X] Boxing
- [X] Breakout
- [X] Carnival
- [X] Centipede
- [ ] Chopper Command  (only vision)
- [ ] DemonAttack  (only vision)
- [ ] Fishing Derby  (only vision)
- [X] Freeway
- [ ] Frostbite  (only vision)
- [X] Kangaroo
- [X] MontezumaRevenge
- [X] MsPacman
- [ ] Pitfall  (only vision)
- [X] Pong
- [ ] PrivateEye  (only vision)
- [ ] Q\*Bert  (only vision)
- [ ] RiverRaid  (only vision)
- [ ] RoadRunner  (only vision)
- [X] Seaquest
- [X] Skiing
- [X] Space Invaders
- [X] Tennis

## Install
You can install OCAtari in multiple ways, the easiest is to use the provided Dockerfile to install all requirements, like the Atari ROMs and gymnasium.

If you have full control, we provide the following step-by-step installation manual:

`python setup.py install` or `python setup.py develop`

## Usage

```python
from ocatari.core import OCAtari
env = OCAtari("Pong", mode="vision", hud=True, render_mode='rgb_array')
observation, info = env.reset()
obs, reward, terminated, truncated, info = env.step(1)
```

### The two modes of OCAtari
OCAtari supports two different modes to extract objects from the current state:

**Vision mode:** Return a list of objects currently on the screen with their X, Y, Width, Height, R, G, B Values, based on handwritten rules used on the visual representation. 

**Ram/Revised mode:** Uses the object values stored in the RAM to detect the objects currently on the screen.

### Use these trained agents and the demo script:

A better example how to run OCAtari is given with our demo files showing you how to run each game with a provided agent. 

Use the demo files in the scripts/demo folder to test it yourself. You can set the mode to 'raw', 'vision' or 'revised' in line 10 of the demo script.
You can also run the demo file with an already trained agent or your own developed agent. You can use the -p flag in the command to run the demo file by an agent and let the agent play the game.
Here is an example: 

`python3.8 demo_pong.py -p models/Pong/model_50000000.gz`

### Extract the objects from a state 

With `env.objects` one can access the list of objects found in the current state. Note that these lists can differ depending on the mode you used initiating the environment

### Producing your own dataset

OCAtari can be used to generate datasets consisting of a represenation of the current state in form of an RGB array and a list of all objects within the state. 
More information can be found in the dataset_generation folder. 

## Models and additional Information

As trained agents as well as to reproduce our results, we recomment to use the agents of [this repo](https://github.com/floringogianu/atari-agents).  

### Reproducing our results
In most of our scripts we added the following line to make the deterministic and easier to reproduce `make_deterministic(env, 42)`. This line can and should be removed if this is not the desired behavior. 
As seeds we used 0 for evaluating the metrics and 42 for generating the dataset. 

