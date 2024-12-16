# ODA: An object-centric dataset for Atari

## Using generate_dataset.py
`generate_dataset.py`is the main script for generating object-centric datasets for Atari games. The list of supported games can be found in the OCAtari ReadMe. Games which only supports vision mode should use the `generate_dataset_vision.py`script instead. All parameters and settings are identical and can be used with both scripts.


### Requirements
It is necessary to keep the structure of the repository intact so that the scripts can find the required DQN models. All models needed for generation are also part of the repository and can be found under /OCAtari/models/{game}/dqn.gz.

To run the scripts, it is also necessary to go through the installation process of the repository and thus install the necessary ROMs of the games.

### Parameters
`generate_dataset.py` and `generate_dataset_vision.py` have the following parameters:

* `-g` or `--game`: game to evaluate (e.g. 'Pong')
* `-i` or `--interval` : The frame export interval (default is 1, i.e., export every frame)
* `-hud`: Should the HUD elements also be detected (default is True)
* `-dqn`: Should the default dqn model (../models/{game}/dqn.gz) be used or a different model (in this case a path has to be provided)

Example: `generate_dataset.py -g Pong`


## Information within the datasets
The data set consists primarily of a csv file. In addition to a sequential **index**, this file contains the respective image as a list of pixels, called **OBS**. This list can be reformerd into into a numpy array by
`np.array([int(x) for x in dataframe.iloc[x]["OBS"][1:-1].split(",")]).reshape(210,160,3)`
and can thus be processed further. An image in the form of a png is also stored separately. Furthermore, the CSV file contains a list of all HUD elements that could be extracted from the RAM, called **HUD**, as well as a list of all objects that were read from the RAM, called **RAM**. Finally, we provide a list of all elements that could be generated using the vision mode, called **VIS**.


## Reproducing ODA
The ODA mentioned within the paper, is a small dataset of 10,000 samples per supported game. To reproduce the exact dataset you have to set the generation process to deterministic `make_deterministic(42, env)` and start the dataset generation. We used the seed `42`.

The easiest way is to generate the dataset for all supported games, run the `datasets_on_all.sh`script, generating the exact dataset.
