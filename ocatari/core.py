from collections import deque
from typing import Tuple

import gymnasium as gym
from termcolor import colored
import numpy as np
from ocatari.ram.extract_ram_info import detect_objects_ram, init_objects, \
    get_max_objects, instantiate_max_objects, get_class_dict, get_object_state, get_object_state_size
from ocatari.vision.extract_vision_info import detect_objects_vision
from ocatari.vision.utils import mark_bb, to_rgba
from ocatari.ram.game_objects import GameObject, ValueObject
from ocatari.vision.game_objects import GameObject as GameObjectVision
from ocatari.utils import draw_label, draw_arrow, draw_orientation_indicator
from gymnasium.error import NameNotFound
from itertools import chain

try:
    import ale_py
except ModuleNotFoundError:
    print(
        '\nALE is required when using the ALE env wrapper. ',
        'Try `pip install "gymnasium[atari, accept-rom-license]"`.\n',
    )

import warnings

UPSCALE_FACTOR = 4


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
    _tensor = torch.tensor
    _uint8 = torch.uint8
    _zeros = torch.zeros
    _zeros_like = torch.zeros_like
    _stack = torch.stack
    DEVICE = "cpu" if torch.cuda.is_available() else "cpu"
    _tensor_kwargs = {"device": DEVICE}
except ModuleNotFoundError:
    torch_imported = False
    _tensor = np.array
    _uint8 = np.uint8
    _zeros = np.zeros
    _zeros_like = np.zeros_like
    _stack = np.stack
    DEVICE = "cpu"
    _tensor_kwargs = {}
    warnings.warn("pytorch installation not found, using numpy instead of torch")

try:
    import pygame
except ModuleNotFoundError:
    print(
        "\npygame is required for human rendering. ",
        "Try `pip install pygame`.\n",
    )

if torch_imported:
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
else:
    DEVICE = "cpu" 
    
AVAILABLE_GAMES = ["Adventure", "Alien", "Amidar", "Assault", "Asterix", 
                   "Asteroids", "Atlantis", "BankHeist", "BattleZone",
                   "BeamRider", "Berzerk", "Bowling", "Boxing",
                   "Breakout", "Carnival", "Centipede", "ChopperCommand", 
                   "CrazyClimber", "DemonAttack", "DonkeyKong",
                   "DoubleDunk", "Enduro", "FishingDerby", "Freeway",                   
                   "Frostbite", "Galaxian", "Gopher", "Hero", "IceHockey", 
                   "Jamesbond", "Kangaroo", "Krull", "KungFuMaster", "MontezumaRevenge", 
                   "MsPacman", "NameThisGame","Pacman", "Phoenix","Pitfall", "Pong", "Pooyan", "PrivateEye",
                   "Qbert", "Riverraid", "RoadRunner", "Seaquest", "Skiing", 
                   "SpaceInvaders", "Tennis", "TimePilot", "UpNDown", "Venture", 
                   #"Videocube", 
                   "VideoPinball", "YarsRevenge", "Zaxxon"]


# TODO: complete the docstring 
class OCAtari:
    """
    The OCAtari environment. Initialize it to get a Atari environments with objects tracked.

    :param env_name: The name of the Atari gymnasium environment e.g. "Pong" or "PongNoFrameskip-v5"
    :type env_name: str
    :param mode: The detection method type: one of `raw`, `ram`, or `vision`, or `both` (i.e. `ram` + `vision`)
    :type mode: str
    :param hud: Whether to include or not objects from the HUD (e.g. scores, lives)
    :type hud: bool
    :param obs_mode: Define the observation mode. Set to `dqn` (84x84, grayscaled), `ori` (210x160x3, RGB image), `obj` (#Objectsx4). `dqn` and `ori` are also organized in a stack of the last 4 frames.
    :type obs_mode: str
    
    the remaining \*args and \**kwargs will be passed to the \
        `gymnasium.make <https://gymnasium.farama.org/api/registry/#gymnasium.make>`_ function.
    """
    def __init__(self, env_name, mode="ram", hud=False, obs_mode="ori",
                 render_mode=None, render_oc_overlay=False, *args, **kwargs):
        if "ALE/" in env_name: #case if v5 specified
            to_check = env_name[4:8]
            game_name = env_name.split("/")[1].split("-")[0].split("No")[0].split("Deterministic")[0]
        else:
            to_check = env_name[:4]
            game_name = env_name.split("-")[0].split("No")[0].split("Deterministic")[0]
        if to_check[:4] not in [gn[:4] for gn in AVAILABLE_GAMES]:
            print(colored(f"Game '{env_name}' not covered yet by OCAtari", "red"))
            print("Available games: ", AVAILABLE_GAMES)
            self._covered_game = False
        else:
            self._covered_game = True
        
        gym_render_mode = "rgb_array" if render_oc_overlay else render_mode
        self._env = gym.make(env_name, render_mode=gym_render_mode, *args, **kwargs)
        self.game_name = game_name
        self.mode = mode
        self.obs_mode = obs_mode
        self.hud = hud
        self.max_objects_per_cat = get_max_objects(self.game_name, self.hud)
        self.buffer_window_size = 4
        self.step = self._step_impl
        if not self._covered_game:
            print(colored("\n\n\tUncovered game !!!!!\n\n", "red"))
            global init_objects
            init_objects = lambda *args, **kwargs: []
            self.detect_objects = lambda *args, **kwargs: None
            self.objects_v = []
        elif mode == "vision":
            self.detect_objects = self._detect_objects_vision
            self._objects : list[GameObjectVision] = init_objects(self.game_name, self.hud, vision=True)
        elif mode == "revised" or mode== "ram" :
            if mode == "revised":
                warnings.warn("'revised' mode will deprecate with the next major update, please use 'ram' mode instead.", DeprecationWarning)
            self.detect_objects = self._detect_objects_ram
            self._objects : list[GameObject] = init_objects(self.game_name, self.hud)
        elif mode == "both":
            self.detect_objects = self._detect_objects_both
            self.objects_v = init_objects(self.game_name, self.hud)
        else:
            import ipdb;ipdb.set_trace()
            print(colored("Undefined mode for information extraction", "red"))
            exit(1)
        self._class_dict = get_class_dict(self.game_name)
        self._slots_str = [c for c, n in self.max_objects_per_cat.items() for i in range(n)]
        self._slots = [self._class_dict[c]() for c in self._slots_str]
        self._ns_state = np.zeros(sum([len(o._nsrepr) for o in self._slots]))
        self.ns_meaning = [f"{o.category} ({o._ns_meaning})" for o in self._slots]
        if obs_mode == "dqn":
            if torch_imported:
                self._env.observation_space = gym.spaces.Box(0, 255, (4, 84, 84), dtype=np.uint8)
            else:
                print("To use the buffer DQN of OCAtari, you need to install torch.")
        elif obs_mode == "obj":
            print("Using OBJ State Representation")
            # if mode == "ram":
            self.buffer_window_size = 2
            ocss = get_object_state_size(self.game_name, self.hud)
            self._env.observation_space = gym.spaces.Box(0, 255, (self.buffer_window_size, ocss), dtype=np.uint8)
            self.reference_list = []
            for k in list(self.max_objects_per_cat.keys()):
                self.reference_list.extend([k for i in range(self.max_objects_per_cat[k])])
            # else:
            #     print(colored("This obs mode is only available in ram mode", "red"))
            #     exit(1)
        # elif obs_mode is not None:
            # import ipdb;ipdb.set_trace()
            # print(colored("Undefined mode for observation (obs_mode), has to be one of ['dqn', 'ori', None]", "red"))
            # exit(1)

        self.render_mode = render_mode
        self.render_oc_overlay = render_oc_overlay
        self.rendering_initialized = False

        self._state_buffer_rgb = deque([], maxlen=self.buffer_window_size)
        self._state_buffer_ns = deque([], maxlen=self.buffer_window_size)
        self.action_space = self._env.action_space
        self._ale = self._env.unwrapped.ale
        # inhererit every attribute and method of env
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
        Fills the buffer if `obs_mode` was not None at initialization. The observations follow the `obs_mode`. \
        The method runs the Atari environment `env.step() <https://gymnasium.farama.org/api/env/#gymnasium.Env.step>`_ method
        
        :param action: The action to perform at this step.
        :type action: int
        """
        raise NotImplementedError()

    def _step_impl(self, *args, **kwargs):
        obs, reward, terminated, truncated, info = self._env.step(*args, **kwargs)
        self.detect_objects()
        self._fill_buffer()
        return obs, reward, truncated, terminated, info
    
    def _detect_objects_ram(self):
        detect_objects_ram(self._objects, self._env.env.unwrapped.ale.getRAM(), self.game_name, self.hud)

    def _detect_objects_vision(self):
        detect_objects_vision(self._objects, self._env.env.unwrapped.ale.getScreenRGB(), self.game_name, self.hud)

    def _detect_objects_both(self):
        detect_objects_ram(self._objects, self._env.env.unwrapped.ale.getRAM(), self.game_name, self.hud)
        detect_objects_vision(self.objects_v, self._env.env.unwrapped.ale.getScreenRGB(), self.game_name, self.hud)

    def _reset_buffer(self):
        for _ in range(self.buffer_window_size):
            self._fill_buffer()


    def reset(self, *args, **kwargs):
        """
        Resets the buffer and environment to an initial internal state, returning an initial observation and info.
        See `env.reset() <https://gymnasium.farama.org/api/env/#gymnasium.Env.reset>`_ for gymnasium details.
        """
        obs, info = self._env.reset(*args, **kwargs)
        self._objects = init_objects(self.game_name, self.hud, vision=self.mode=="vision")
        self.detect_objects()
        self._reset_buffer()
        return obs, info

    def _fill_buffer(self):
        # rgbstate = self._ale.getScreenRGB()
        self._state_buffer_rgb.append(self._ale.getScreenRGB())
        # self._state_buffer_rgb.append(_tensor(rgbstate, dtype=_uint8,
        #                                   **_tensor_kwargs))
        self._state_buffer_ns.append(self.ns_state)

    def _get_buffer_as_stack(self):
        return _stack(list(self._state_buffer), 0).unsqueeze(0).byte()

    window : pygame.Surface = None
    clock : pygame.time.Clock = None

    def _initialize_rendering(self, sample_image):
        assert sample_image is not None
        pygame.init()
        if self.render_mode == "human":
            pygame.display.set_caption(self.game_name)
        self.image_size = (sample_image.shape[1], sample_image.shape[0])
        self.window_size = (sample_image.shape[1] * UPSCALE_FACTOR,
                            sample_image.shape[0] * UPSCALE_FACTOR)  # render with higher res
        self.label_font = pygame.font.SysFont('Pixel12x10', 16)
        if self.render_mode == "human":
            self.window = pygame.display.set_mode(self.window_size)
            self.clock = pygame.time.Clock()
        else:
            self.window = pygame.Surface(self.window_size)
        self.rendering_initialized = True

    def render(self):
        """
        Compute the render frames (as specified by render_mode during the
        initialization of the environment). If activated, adds an overlay visualizing
        object properties like position, velocity vector, orientation, name, etc.
        See `env.render() <https://gymnasium.farama.org/api/env/#gymnasium.Env.render>`_
        for gymnasium details.
        """

        image = self._env.render()

        if not self.render_oc_overlay:
            if self.rendering_initialized:
                return image.swapaxes(0,1).repeat(UPSCALE_FACTOR, axis=0).repeat(UPSCALE_FACTOR, axis=1)
            return image

        else:
            # Prepare screen if not initialized
            if not self.rendering_initialized:
                self._initialize_rendering(image)

            # Render env RGB image
            image = np.transpose(image, (1, 0, 2))
            image_surface = pygame.Surface(self.image_size)
            pygame.pixelcopy.array_to_surface(image_surface, image)
            upscaled_image = pygame.transform.scale(image_surface, self.window_size)
            self.window.blit(upscaled_image, (0, 0))

            # Init overlay surface
            overlay_surface = pygame.Surface(self.window_size)
            overlay_surface.set_colorkey((0, 0, 0))

            # For each object, render its position and velocity vector
            for game_object in self.objects:
                # if game_object is None:
                #     continue

                x, y = game_object.xy
                w, h = game_object.wh

                if x == np.nan:
                    continue

                # Object velocity
                dx = game_object.dx
                dy = game_object.dy

                # Transform to upscaled screen resolution
                x *= UPSCALE_FACTOR
                y *= UPSCALE_FACTOR
                w *= UPSCALE_FACTOR
                h *= UPSCALE_FACTOR
                dx *= UPSCALE_FACTOR
                dy *= UPSCALE_FACTOR

                # Compute center coordinates
                x_c = x + w // 2
                y_c = y + h // 2

                # # Draw an 'X' at object center
                # pygame.draw.line(overlay_surface, color=(255, 255, 255), width=2,
                #                  start_pos=(x_c - 4, y_c - 4), end_pos=(x_c + 4, y_c + 4))
                # pygame.draw.line(overlay_surface, color=(255, 255, 255), width=2,
                #                  start_pos=(x_c - 4, y_c + 4), end_pos=(x_c + 4, y_c - 4))

                # Draw bounding box
                pygame.draw.rect(overlay_surface, color=game_object.rgb,
                                 rect=(x, y, w, h), width=2)

                # Draw object category label (optional with value)
                label = game_object.category
                if isinstance(game_object, ValueObject):
                    label += f" ({game_object.value})"
                draw_label(self.window, label, position=(x, y + h + 4), font=self.label_font)

                # Draw object orientation
                # if game_object.orientation is not None:
                #     draw_orientation_indicator(overlay_surface, game_object.orientation.value, x_c, y_c, w, h)

                # Draw velocity vector
                if dx != 0 or dy != 0:
                    draw_arrow(overlay_surface,
                               start_pos=(float(x_c), float(y_c)),
                               end_pos=(x_c + 2 * dx, y_c + 2 * dy),
                               color=(100, 200, 255),
                               width=2)

            self.window.blit(overlay_surface, (0, 0))

            if self.render_mode == "human":
                frameskip = self._env.unwrapped._frameskip if isinstance(self._env.unwrapped._frameskip, int) else 1
                self.clock.tick(60 // frameskip)  # limit FPS to avoid super fast movement
                pygame.display.flip()
                pygame.event.pump()

            elif self.render_mode == "rgb_array":
                return pygame.surfarray.array3d(self.window)

    def close(self, *args, **kwargs):
        """
        After the user has finished using the environment, close contains the code necessary to "clean up" the environment.
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
        return self.action_space.n

    @property
    def dqn_obs(self):
        """
        The 4 (grey+down)scaled last frames (84x84) of the environment, used notably by dqn agents as states.

        :type: torch.tensor
        """
        dqn_obs = [_tensor(cv2.resize(cv2.cvtColor(rgbs, cv2.COLOR_RGB2GRAY), 
                                      (84, 84), interpolation=cv2.INTER_AREA), 
                           dtype=_uint8, **_tensor_kwargs) for rgbs in self._state_buffer_rgb]
        return _stack(list(dqn_obs), 0).unsqueeze(0).byte()

    
    @property
    def get_rgb_state(self):
        """
        :type: np.array
        """
        return self._ale.getScreenRGB()
    

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

    def getScreenRGB(self):
        return self.env.unwrapped.ale.getScreenRGB()
    
    def detect_objects_both(self):
        detect_objects_ram(self.objects, self._env.env.unwrapped.ale.getRAM, self.game_name, self.hud)
        detect_objects_vision(self.objects_v, self._env.env.unwrapped.ale.getScreenRGB, self.game_name, self.hud)

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
        return self._env.env.env.ale.restoreSystemState(state)
    
    @property
    def ns_state(self):
        """
        Returns the current neurosymbolic state of the environment.
        
        :return: State snapshot
        :rtype: env_snapshot
        """

        return list(chain.from_iterable([o._nsrepr for o in self._objects]))
        
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
        rendered = _zeros_like(self._state_buffer[0]).float()
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
        rendered = _zeros_like(self._state_buffer[0]).float()
        for coef, state_i in zip(coefs, self._state_buffer):
            rendered += coef * state_i
        rendered = rendered.cpu().detach().to(int).numpy()
        return rendered
