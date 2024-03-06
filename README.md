# Object-Centric Atari Environments
Quentin Delfosse, Jannis Blüml, Bjarne Gregori, Sebastian Sztwiertnia, Anurag Maurya, Kévin-Lâm Quesnel and Simon Wulf

<img style="float: right;" width="400px" align="right" src="docs/_static/kangaroo.png">

Inspired by thw work of [Anand et. al.](https://arxiv.org/abs/1906.08226), we present OCAtari, an improved, extended and object-centric version of their [ATARI ARI project](https://github.com/mila-iqia/atari-representation-learning). \
The [Arcade Learning Environment](https://github.com/mgbellemare/Arcade-Learning-Environment) allows us to read the RAM state at any time of a game. 
This repository provides a wrapper for the well known [Gynmasium project](https://github.com/Farama-Foundation/Gymnasium), that uses the state of the ram and reverse engineering to provide object centric representation of the screen. It provides code for benchmarking, testing and generating object-centric representations of states.

* [Install](#install) -- Install all relevant dependencies and start using OCAtari yourself
* [Usage](#usage) -- Learn about the different environments OCAtari supports and enables
* [Producing your own dataset](#producing-your-own-dataset) -- OCAtari also support the generation of object-centric datasets for supported Atari games
* [Models and additional Information](#models-and-additional-information) -- Everything you need to know to reproduce our results


:heavy_exclamation_mark: [HERE IS A LINK TO THE DOCUMENTATION  :bookmark_tabs:](https://oc-atari.readthedocs.io/en/latest/)

--- 

### Structure of this repository
This repository is structured into multiple folder:
* [dataset_generation](dataset_generation/) -- includes all scripts needed to generate object-centric datasets for Atari game
* [models](models/) -- includes all models needed to reproduce our results as well as to test out the environments
* [ocatari](ocatari/) -- the actual wrapper
* [scripts](scripts/) -- A huge amount of scripts to help and test while implementing, extending or using OCAtari. 
Most are used to reverse engineer the RAM state, like searching for correlations within the RAM state.


## Install
You can install OCAtari in multiple ways, the recommended is to use the provided Dockerfile to install all requirements, like the Atari ROMs and gymnasium.
You can also simply:
`pip install ocatari`
`pip install "gymnasium[atari, accept-rom-license]"`
If you want to modify the code, you can clone this repo and run:
`python setup.py install` or if you want to modify the code `python setup.py develop`


## Usage
To use the OCAtari environments:
``` python
from ocatari.core import OCAtari
import random

env = OCAtari("Pong", mode="ram", hud=True, render_mode="rgb_array")
observation, info = env.reset()
action = random.randint(0, env.nb_actions-1)
obs, reward, terminated, truncated, info = env.step(action)
```

### Cite OCAtari:
If you are using OCAtari for your scientific pubplease use 'ram' mode insteadlications, please cite us:
```bibtex
@inproceedings{Delfosse2023OCAtariOA,
title={OCAtari: Object-Centric Atari 2600 Reinforcement Learning Environments},
author={Quentin Delfosse and Jannis Blüml and Bjarne Gregori and Sebastian Sztwiertnia and Kristian Kersting},
year={2023}
}
```

###  List of covered games
- [X] Alien
- [X] Amidar
- [X] Assault
- [X] Asterix
- [X] Asteroids  (only vision)
- [X] Atlantis
- [ ] BattleZone (in progress)
- [ ] Bankheist (in progress)
- [ ] BeamRider  (only vision)
- [X] Berzerk
- [X] Bowling
- [X] Boxing
- [X] Breakout
- [X] Carnival
- [X] Centipede
- [X] Chopper Command
- [X] Crazy Climbers
- [X] DemonAttack
- [X] DonkeyKong
- [X] Fishing Derby  
- [X] Freeway
- [X] Frostbite
- [X] Gopher
- [X] Hero
- [X] IceHockey
- [X] Kangaroo
- [X] Krull
- [X] MontezumaRevenge
- [X] MsPacman
- [X] Pacman
- [X] Pitfall
- [X] Pong
- [X] PrivateEye
- [X] Q\*Bert  
- [X] RiverRaid  
- [X] RoadRunner  
- [X] Seaquest
- [X] Skiing
- [X] Space Invaders
- [X] Tennis
- [X] Time Pilot
- [X] Up n Down (in progress)
- [X] Venture
- [X] VideoPinball
- [ ] YarsRevenge (in progress)

A list of all gymnasium games can be found in the [Gymnasium Documentation](https://gymnasium.farama.org/environments/atari/)

### The two modes of OCAtari
OCAtari supports two different modes to extract objects from the current state:

**Vision Extraction Mode (VEM):** Return a list of objects currently on the screen with their X, Y, Width, Height, R, G, B Values, based on handwritten rules used on the visual representation. 

**Ram Extraction Mode (REM):** Uses the object values stored in the RAM to detect the objects currently on the screen.

### Use these trained agents and the demo script:

A better example how to run OCAtari is given with our demo files showing you how to run each game with a provided agent. 

Use the demo files in the scripts/demo folder to test it yourself. You can set the mode to 'raw', 'vision' or 'revised' in line 10 of the demo script.
You can also run the demo file with an already trained agent or your own developed agent. You can use the -p flag in the command to run the demo file by an agent and let the agent play the game.
Here is an example: 

`python demo_pong.py -p models/Pong/model_50000000.gz`

More information can be found in this [ReadMe](scripts/demo/README%20Demos.md)

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

