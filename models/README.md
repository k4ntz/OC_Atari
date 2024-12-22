# Usage of Trained Agents

This guide explains how to use the pre-trained agents for Atari games using OCAtari. The models must be downloaded and can be used with the provided script from the script folder.

---

## **1. Downloading the Models**

The trained models can be downloaded from the following link:

[Download Models](https://hessenbox.tu-darmstadt.de/getlink/fiMp3RajkfxCvHXY8zFGC8VW/)

Ensure that the downloaded models are placed in the appropriate directory, such as `OCAtari/models/` or another path of your choosing.

---

## **2. Running the Agents**

Use the `scripts/run_agent.py` script to evaluate the pre-trained agents. The script supports specifying the game, model, and configuration options.

### **Command Structure**
```bash
python scripts/run_agent.py -g <GAME_NAME> -a <MODEL_PATH> -w <WINDOW_SIZE> -f <FRAMESKIP> -o <OBS_MODE>
```
- **`<GAME_NAME>`**: Name of the Atari game (e.g., `Skiing-v4`, `Freeway`, `ALE/Freeway`, `ALE/Skiing-v5`, ...). The `ALE` in front of the name specifies the newer v5 version.
- **`<MODEL_PATH>`**: Path to the trained model file
- **`<WORKERS>`**: Number of images in the stack (Default is 2 for obj and 4 for dqn-like)
- **`<FRAMESKIP>`**: Number of frames to skip (Default in v5 is 4)
- **`<ALGORITHM>`**: Observation mode (`dqn` or `obj`)

### **Example Commands**

#### 2. Running PPO on ALE/Freeway
```bash
python scripts/run_agent.py -g ALE/Freeway -a models/Freeway/42/pixel_ppo.cleanrl_model -w 4 -f 4 -o dqn
```

#### 4. Running Object-Centric PPO on Skiing
```bash
python scripts/run_agent.py -g ALE/Skiing -a models/Skiing/42/obj_ppo.cleanrl_model -w 2 -f 4 -o obj
```

---

## ** 3. Use your own models with OCAtari**
* Check out the `run_agent` script and replace the `load_agent` method with your own agent definition
* Set the parameters to match your model training environment (frameskip, window_size, model)
* Replace the policy with your predict method or a like


## **4. Notes**
- Ensure all dependencies are installed (e.g., `gymnasium`, `ale-py`, `torch`).
- Verify the model paths are correct relative to your script.
- For headless environments, consider using virtual display tools like `Xvfb`.
- More config settings can be found in the script itself, e.g., if you want to record a video of a run.

---

## **5. Troubleshooting**

### **Issue: `Missing ROMS`**
* Check if you install gymnasium with the correct parameters `pip install "gymnasium[atari, accept-rom-license]"`

### **Misshape in the neural network**
* Check that you used the correct parameters (-w, -f, -o) for the model you want to use

---

For further assistance, please reach out to the maintainers or consult the project documentation.
