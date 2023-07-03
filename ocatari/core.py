from collections import deque

import gymnasium as gym
from termcolor import colored
import numpy as np
from ocatari.ram.extract_ram_info import detect_objects_raw, detect_objects_revised, init_objects, get_max_objects
from ocatari.vision.extract_vision_info import detect_objects_vision
from ocatari.vision.utils import mark_bb, to_rgba

try:
    import cv2
except ModuleNotFoundError:
    print(
        "\nOpenCV is required when using the ALE env wrapper. ",
        "Try `pip install opencv-python`.\n",
    )
try:
    import torch
    torch_imported = True
except ModuleNotFoundError:
    torch_imported = False

DEVICE = "cpu"

AVAILABLE_GAMES = ["Alien", "Assault", "Asterix", "Asteroids", "Atlantis", "BeamRider", "Berzerk", "Bowling", "Boxing",
                   "Breakout", "Carnival", "Centipede", "ChoppperCommand", "DemonAttack", "FishingDerby", "Freeway",
                   "Frostbite", "Hero", "Kangaroo",
                   "MontezumaRevenge", "MsPacman","Pitfall", "Pong", "Qbert", "Riverraid", "RoadRunner", "Seaquest", "Skiing",
                   "SpaceInvaders",
                   "Tennis","Yarsrevenge"]


# TODO: complete the docstring 
class OCAtari:
    """
    The OCAtari environment. Initialize it to get a Atari environments with objects tracked.

    :param env_name: The name of the Atari gymnasium environment e.g. "Pong" or "PongNoFrameskip-v5"
    :type env_name: str
    :param mode: The detection method type: one of `raw`, `revised`, or `vision`, or `both` (i.e. `revised` + `vision`)
    :type mode: str
    :param hud: Wether to include or not objects from the HUD (e.g. scores, lives)
    :type hud: bool
    :param obs_mode: How to fill the image buffer (contaning the 4 last frames): one of `None`, `dqn`, `ori` 
    :type obs_mode: str
    
    the remaining \*args and \**kwargs will be passed to the \
        `gymnasium.make <https://gymnasium.farama.org/api/registry/#gymnasium.make>`_ function.
    """
    def __init__(self, env_name, mode="raw", hud=False, obs_mode="dqn", *args, **kwargs):
        if "ALE/" in env_name: #case if v5 specified
            to_check = env_name[4:8]
            game_name = env_name.split("/")[1].split("-")[0].split("No")[0].split("Deterministic")[0]
        else:
            to_check = env_name[:4]
            game_name = env_name.split("-")[0].split("No")[0].split("Deterministic")[0]
        if to_check[:4] not in [gn[:4] for gn in AVAILABLE_GAMES]:
            print(colored("Game not available in OCAtari", "red"))
            print("Available games: ", AVAILABLE_GAMES)
            exit(1)
        self._env = gym.make(env_name, *args, **kwargs)
        self.game_name = game_name
        self.mode = mode
        self.obs_mode = obs_mode
        self.hud = hud
        self.max_objects = []
        self._objects = init_objects(self.game_name, self.hud)
        if mode == "vision":
            self.detect_objects = detect_objects_vision
            self.step = self._step_vision
        elif mode == "raw":
            self.detect_objects = detect_objects_raw
            self.step = self._step_ram
        elif mode == "revised":
            self.max_objects = get_max_objects(self.game_name, self.hud)
            self.detect_objects = detect_objects_revised
            self.step = self._step_ram
        elif mode == "both":
            self.detect_objects_v = detect_objects_vision
            self.detect_objects_r = detect_objects_revised
            self.objects_v = init_objects(self.game_name, self.hud)
            self.step = self._step_test
        else:
            print(colored("Undefined mode for information extraction", "red"))
            exit(1)
        self._fill_buffer = lambda *args, **kwargs: None
        self._reset_buffer = lambda *args, **kwargs: None
        if obs_mode == "dqn":
            if torch_imported:
                self._fill_buffer = self._fill_buffer_dqn
                self._reset_buffer = self._reset_buffer_dqn
            else:
                print("To use the buffer of OCAtari, you need to install torch.")
        elif obs_mode == "ori":
            self._fill_buffer = self._fill_buffer_ori
            self._reset_buffer = self._reset_buffer_ori
        elif obs_mode is not None:
            print(colored("Undefined mode for observation (obs_mode), has to be one of ['dqn', 'ori', None]", "red"))
            exit(1)
        self.window = 4
        self._state_buffer = deque([], maxlen=self.window)
        self.action_space = self._env.action_space
        self._ale = self._env.unwrapped.ale
        #inhererit every attribute and method of env
        for meth in dir(self._env):
            if meth not in dir(self):
                try:
                    setattr(self, meth, getattr(self._env, meth))
                except AttributeError:
                    pass

    def step(self, *args, **kwargs):
        """
        Run one timestep of the environment's dynamics using the agent actions. \
        Extracts the objects, using RAM or vision based on the `mode` variable set at initialization. \
        Fills the buffer if `obs_mode` was not None at initialization. \
        The runs the Atari environment `env.step() <https://gymnasium.farama.org/api/env/#gymnasium.Env.step>`_ method
        
        :param action: The action to perform at this step.
        :type action: int
        """
        raise NotImplementedError()

    def _step_ram(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        if self.mode == "revised":
            self.detect_objects(self._objects, self._env.env.unwrapped.ale.getRAM(), self.game_name, self.hud)
        else:  # mode == "raw" because in raw mode we augment the info dictionary
            self.detect_objects(info, self._env.env.unwrapped.ale.getRAM(), self.game_name)
        self._fill_buffer()
        # if self.obs_mode in ["dqn", "ori"]:
        #     obs = self._get_buffer_as_stack()
        return obs, reward, truncated, terminated, info

    def _step_vision(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        self.detect_objects(self._objects, obs, self.game_name, self.hud)
        self._fill_buffer()
        # if self.obs_mode in ["dqn", "ori"]:
        #     obs = self._get_buffer_as_stack()
        return obs, reward, truncated, terminated, info

    def _step_test(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        self.detect_objects_r(self._objects, self._env.env.unwrapped.ale.getRAM(), self.game_name, self.hud)
        self.detect_objects_v(self.objects_v, obs, self.game_name, self.hud)
        self._fill_buffer()
        # if self.obs_mode in ["dqn", "ori"]:
        #     obs = self._get_buffer_as_stack()
        return obs, reward, truncated, terminated, info

    def _reset_buffer_dqn(self):
        for _ in range(self.window):
            self._state_buffer.append(
                torch.zeros(84, 84, device=DEVICE, dtype=torch.uint8)
            )

    def _reset_buffer_ori(self):
        for _ in range(self.window):
            self._state_buffer.append(
                torch.zeros(210, 160, 3, device=DEVICE, dtype=torch.uint8)
            )

    def reset(self, *args, **kwargs):
        """
        Resets the buffer and environment to an initial internal state, returning an initial observation and info.
        See `env.reset() <https://gymnasium.farama.org/api/env/#gymnasium.Env.reset>`_ for gymnasium details.
        """
        self._reset_buffer()
        self._objects = init_objects(self.game_name, self.hud)
        return self._env.reset(*args, **kwargs)

    def _fill_buffer_dqn(self):
        state = cv2.resize(
            self._ale.getScreenGrayscale(), (84, 84), interpolation=cv2.INTER_AREA,
        )
        self._state_buffer.append(torch.tensor(state, dtype=torch.uint8,
                                               device=DEVICE))

    def _fill_buffer_ori(self):
        state = self._ale.getScreenRGB()
        self._state_buffer.append(torch.tensor(state, dtype=torch.uint8,
                                               device=DEVICE))

    def _get_buffer_as_stack(self):
        return torch.stack(list(self._state_buffer), 0).unsqueeze(0).byte()
    
    def render(self, *args, **kwargs):
        """
        After the user has finished using the environment, close contains the code necessary to "clean up" the environment.
        See `env.render() <https://gymnasium.farama.org/api/env/#gymnasium.Env.render>`_ for gymnasium details.
        """
        return self._env.render(*args, **kwargs)

    def close(self, *args, **kwargs):
        """
        Compute the render frames as specified by render_mode during the initialization of the environment.
        See `env.close() <https://gymnasium.farama.org/api/env/#gymnasium.Env.close>`_ for gymnasium details.
        """
        return self._env.close(*args, **kwargs)

    def seed(self, seed, *args, **kwargs):
        self._env.seed(seed, *args, **kwargs)

    @property
    def nb_actions(self):
        """
        The number of actions available in this environments.

        :type: int
        """
        return self._env.unwrapped.action_space.n

    @property
    def dqn_obs(self):
        """
        The 4 (grey+down)scaled last frames (84x84) of the environment, used notably by dqn agents as states.

        :type: torch.tensor
        """
        return self._get_buffer_as_stack()

    def set_ram(self, target_ram_position, new_value):
        """
        Directly set a given value at a targeted RAM position.

        :param target_ram_position: The ram position to be altered
        :type target_ram_position: int
        :param new_value: The value to put at this RAM position
        :type new_value: int
        """
        return self._env.unwrapped.ale.setRAM(target_ram_position, new_value)

    def get_ram(self):
        """
        Returns the RAM state

        :return: The 128 list of RAM bytes
        :rtype: list of 128 uint8 values
        """
        return self._ale.getRAM()

    def get_action_meanings(self):
        return self._env.env.env.get_action_meanings()

    def _get_obs(self):
        return self._env.env.env.unwrapped._get_obs()

    def _clone_state(self):
        """
        Returns the current system_state of the environment.
        
        :return: State snapshot
        :rtype: env_snapshot
        """
        return self._env.env.env.ale.cloneSystemState()

    def _restore_state(self, state):
        """
        Restore the current system_state of the environment.
        
        :param state: State snapshot to be restored
        :type state: env_snapshot
        """
        return self._env.env.env.ale.cloneSystemState()

    @property
    def objects(self):
        """
        A list of the object present in the environment. The objects are either \
        ocatari.vision.GameObject or ocatari.ram.GameObject, depending on the extraction method.

        :type: list of GameObjects
        """
        return [obj for obj in self._objects if obj] # filtering out None objects

    def render_explanations(self):
        coefs = [0.05, 0.1, 0.25, 0.6]
        rendered = torch.zeros_like(self._state_buffer[0]).float()
        for coef, state_i in zip(coefs, self._state_buffer):
            rendered += coef * state_i
        rendered = rendered.cpu().detach().to(int).numpy()
        for obj in self.objects:
            mark_bb(rendered, obj.xywh, color=obj.rgb)
        import matplotlib.pyplot as plt
        plt.imshow(rendered)
        rows, cells, colors = [], [], []
        columns = ["X, Y", "W, H", "R, G, B"]
        for obj in self.objects:
            rows.append(obj.category)
            cells.append([obj.xy, obj.wh, obj.rgb])
            colors.append(to_rgba(obj.rgb))
        # import ipdb; ipdb.set_trace()
        t_height = 0.03 * len(rows)
        table = plt.table(cellText=cells,
                          rowLabels=rows,
                          rowColours=colors,
                          colLabels=columns,
                          colWidths=[.2, .2, .3],
                          bbox=[0.1, 1.02, 0.8, t_height],
                          loc='top')
        table.set_fontsize(14)
        plt.subplots_adjust(top=0.8)
        plt.show()


    def aggregated_render(self, coefs=[0.05, 0.1, 0.25, 0.6]):
        rendered = torch.zeros_like(self._state_buffer[0]).float()
        for coef, state_i in zip(coefs, self._state_buffer):
            rendered += coef * state_i
        rendered = rendered.cpu().detach().to(int).numpy()
        return rendered
