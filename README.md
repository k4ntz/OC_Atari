# OC_Atari

Object-Centric Atari is a Wrapper, based on the [ATARI ARI project](https://github.com/mila-iqia/atari-representation-learning) that uses the state of the ram and reverse engineering to provide object centric representation of the screen. The project supports two different modes for the covered games.

**Vision mode:** Return a list of objects currently on the screen with their X, Y, Width, Height, R, G, B Values. 

**Ram/Revised mode:** Uses the object values stored in the RAM to detect the objects currently on the screen.


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
`python setup.py install` or `python setup.py develop`

## Usage
Use the demo files in the scripts/demo folder. You can set the mode to 'raw', 'vision' or 'revised'.
Test the `demo_pong.py` script.

You can change the `mode` argument line 10!

### Use these trained agents:
You can also run the demo file with an already trained agent or your own developed agent. You can use the -p flag in the command to run the demo file by an agent and let the agent play the game.
Here is an example: 

`python3.8 demo_pong.py -p models/Pong/model_50000000.gz`


## Downloading Trained Atari Agents
For trained agents, we use agents of [this repo](https://github.com/floringogianu/atari-agents)

