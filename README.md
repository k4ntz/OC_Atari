# OC_Atari

Object-Centric Atari is a Wrapper, based on the [ATARI ARI project](https://github.com/mila-iqia/atari-representation-learning) that uses the state of the ram and reverse engineering to provide object centric representation of the screen. The project supports three different modes for the covered games.

**Raw mode**: Annotates the info dictionary with a list of important RAM values (take a look at the comments to see which value represents which variable) and additional information like current score or time.

**Vision mode:** Return a list of objects currently on the screen with their X, Y, Width, Height, R, G, B Values. 

**Revised mode:** Uses the object values stored in the RAM to detect the objects currently on the screen.


## List of covered games

### Priority 1:
- [x]  Breakout
- [x]  Freeway
- [x]  Bowling
- [x]  Ms.Pacman
- [x]  Pong
- [x]  Seaquest
- [x]  Skiing
- [ ]  Space Invaders (worked on by Belal/Sebastian)
- [x]  Asterix
- [ ]  Asteroids (worked on by Chris)
- [x]  Demon Attack
- [x]  Tennis 
- [x]  Kangaroo

### Priority 2:
- [x]  Berzerk
- [ ]  River Raid (worked on by Chris)
- [ ]  Atlantis (worked on by Bjarne)
- [ ]  Chopper Command (worked on by Sebastian)
- [ ]  Q*bert (worked on by Bjarne)
- [ ]  Assault (worked on by Chris)
- [ ]  Beam Rider (worked on by Bjarne)
- [x]  Boxing
- [x]  Carnival
- [x]  Centipede

### Priority 3:
- [ ]  Montezumas Revenge (worked on by Timo)
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
Use the demo files in the scripts/demo folder. You can set the mode to 'raw', 'vision' or 'revised'.
Here is an example:
`python3.8 demo_pong.py`

You can also run the demo file with an already trained agent or your own developed agent. You can use the -p flag in the command to run the demo file by an agent and let the agent play the game.
Here is an example: 
`python3.8 demo_pong.py -p models/Pong/model_50000000.gz`


## Downloading Trained Atari Agents
For trained agents, we use agents of [this repo](https://github.com/floringogianu/atari-agents)

