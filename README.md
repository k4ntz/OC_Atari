# Object-Centric Atari Environments
Quentin Delfosse, Jannis Blüml, Bjarne Gregori, Sebastian Sztwiertnia



<img style="float: right;" width="400px" align="right" src="docs/_static/kangaroo.png">

Inspired by the work of [Anand et. al.](https://arxiv.org/abs/1906.08226), we present OCAtari, an improved, extended, and object-centric version of their [ATARI ARI project](https://github.com/mila-iqia/atari-representation-learning). The [Arcade Learning Environment](https://github.com/mgbellemare/Arcade-Learning-Environment) allows us to read the RAM state at any time of a game. This repository provides a wrapper for the well-known [Gymnasium project](https://github.com/Farama-Foundation/Gymnasium), that uses the state of the RAM and reverse engineering to provide object-centric representation of the screen. It also provides code for benchmarking, testing, and generating object-centric representations of states.

### Features
- Object-centric extraction of Atari game states.
- Vision Extraction Mode (VEM) and RAM Extraction Mode (REM) for object detection.
- Benchmarking and dataset generation tools for Atari environments.

[HERE IS A LINK TO THE DOCUMENTATION  :bookmark_tabs:](https://oc-atari.readthedocs.io/en/latest/)

### Cite OCAtari:
If you are using OCAtari for your scientific publications, please cite us:
```bibtex
@article{delfosse2024ocatari,
    title={{OCAtari}: {O}bject-Centric {Atari} 2600 Reinforcement Learning Environments},
    author={Delfosse, Quentin and Bl{\"{u}}ml, Jannis and Gregori, Bjarne and Sztwiertnia, Sebastian and Kersting, Kristian},
    journal={Reinforcement Learning Journal},
    volume={1},
    pages={400--449},
    year={2024}
}
```

### Structure of this Repository
This repository is structured into multiple folder:
- [Ocatari](ocatari/) -- the actual wrapper
- [Producing your own dataset](dataset_generation/) -- includes all scripts needed to generate object-centric datasets for Atari game
- [Models to use or test with](models/) -- a placeholder folder. put the needed models into to reproduce our results as well as to test out the environments
- [Scripts](scripts/) -- A huge amount of scripts to help and test while implementing, extending or using OCAtari. 
Most are used to reverse engineer the RAM state, like searching for correlations within the RAM state.

---

## Getting Started
Instructions to help users get started with OCAtari.

### Prerequisites
List any software, tools, or dependencies needed to run the project.
For the complete list, see requirements.txt

#### Python
We are currently supporting versions > 3.9

#### Install Gymnasium with Atari support
```sh
pip install "gymnasium[atari, accept-rom-license]"
```

### Installation
You can install OCAtari in multiple ways. The recommended way is to use the provided Dockerfile to install all requirements, such as the Atari ROMs and Gymnasium.
Alternatively, you can install with pip:
```sh
# Install OCAtari
pip install ocatari
```

If you want the current state, please clone the repository and use:

```sh
pip install -e .
```

To modify the code, you can clone/fork this repo and run:

```sh
# Clone the repository
git clone https://github.com/k4ntz/OC_Atari.git

# Navigate to the project directory
cd ocatari

# Install in development mode
python setup.py develop
```

### Usage
To use the OCAtari environments:

```python
from ocatari.core import OCAtari
import random

env = OCAtari("ALE/Pong-v5", mode="ram", hud=True, render_mode="rgb_array")
observation, info = env.reset()
action = random.randint(0, env.nb_actions-1)
obs, reward, terminated, truncated, info = env.step(action)
```

---

## OCAtari Wrapper 
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


### Extracting Objects from a State
With `env.objects`, you can access the list of objects found in the current state. Note that these lists can differ depending on the mode you used when initiating the environment.

####  List of covered games
|          |  AirRaid    |  Alien    |  Amidar    |  Assault  |  Asterix  |  Asteroids  |  Atlantis  |  BankHeist  |  BattleZone  |  BeamR.  |  Berzerk  |  Bowling  |  Boxing  |  Breakout  |  Carnival  |  Centipede  |  ChopperC.  |  CrazyC.  |  DemonA.  |  DonkeyK.  |  DoubleDunk  |  FishingD.  |  Freeway | Frogger |  Frostbite  |  Gopher  |  Hero  |  IceHockey  |  Jamesbond  |  Kangaroo  | KeystoneK.  |  Krull  |  Montezum.  |  MsPacman  |  Pacman  |  Pitfall  |  Pitfall2 |  Pong  |  Pooyan  |  PrivateE.  |  Q*Bert  |  RiverRaid  |  RoadR.  |  Seaquest  |  Skiing  |  SpaceInv.  |  Tennis   |  TimePilot  |  UpNDown  |  Venture  |  VideoP.  |  YarsR.  |
| -------- |  ---------  |  -------  |  --------  |  -------  |  -------  |  ---------  |  --------  |  ---------  |  ----------  |  ------  |  -------  |  -------  |  ------  |  --------  |  --------  |  ---------  |  ---------  |  -------  |  -------  |  --------  |  ----------  |  ---------  |  ------- | ------- |  ---------  |  ------  |  ----  |  ---------  |  ---------  |  --------  |  ---------- |  -----  |  ---------  |  --------  |  ------  |  -------  |  -------  |  ----  |  ------  |  ---------  |  ------  |  ---------  |  ------  |  --------  |  ------  |  ---------  |  -------  |  ---------  |  -------  |  -------  |  -------  |  ------- |
|  Regular |  ✓          |  ✓        |  ✓        |  ✓       |  ✓        |  ✓          |  ✓        |  ✓          |  ❌          |  ✓      |  ✓        |  ✓        |  ✓      |  ✓         |  ✓        |  ✓          |  ✓          |  ✓       |  ✓        |  ✓         |  ✓          |  ✓          |  ✓       |         |  ✓         |  ✓       |  ✓     |  ✓         |  ✓         |  ✓         |             |  ✓      |  ✓         |  ✓         |  ✓      |  ✓        |  ✓        |  ✓    |  ✓       |  ✓         |  ✓       |  ✓         |  ✓       |  ✓        |  ✓       |  ✓         |  ✓        |  ✓         |  ✓        |  ✓        |  ✓       |  ✓       |
|   Slot   |  ✓          |  ✓        |  ✓        |           |  🐏       | 🐏          |  🐏        |  ✓         |              |          |  🐏       |  🐏       |  ✓       |  ✓        |            |             |             |           |  🐏       |   🐏       |              |  🐏         |  🐏      |   👁️     |  ✓         | 🐏       |        | 🐏          |            |  ✓         |   👁️        |         | 🐏          |  ✓         |          |  ✓       |  ✓        |  ✓     |  ✓       |            |          |  🐏         |          |  ✓        |  ✓       |  ✓         |  🐏       |             |           |            |          |          |
* ✓: completed
* 🐛: bug 
* 👁️: only vision
* 🐏: only RAM

A list of all gymnasium games can be found in the [Gymnasium Documentation](https://gymnasium.farama.org/environments/atari/)


### Producing your own dataset

OCAtari can be used to generate datasets consisting of a represenation of the current state in form of an RGB array and a list of all objects within the state. 
More information can be found in the dataset_generation folder. 

### Models and additional Information

As trained agents as well as to reproduce our results, we recomment to use the agents of [this repo](https://github.com/floringogianu/atari-agents) or our [own](https://drive.google.com/drive/folders/1oCLc2cyftDFUepVZewt6msA3ZtLFDViG?usp=drive_link).

### Reproducing our results
As seeds we used 0, 1, 2 for evaluating the metrics and 42, 73, 91 for generating the dataset. Make sure to use the deterministic environments.

---

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/newfeature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/newfeature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
[Quentin Delfosse](mailto:quentin.delfosse@tu-darmstadt.de), [Jannis Blüml](mailto:jannis.blueml@tu-darmstadt.de)

