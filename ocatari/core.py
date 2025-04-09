from collections import deque
import numpy as np
import gymnasium as gym
from itertools import chain
from termcolor import colored
from ocatari.ram.extract_ram_info import (
    detect_objects_ram, init_objects, get_max_objects, get_object_state_size, get_class_dict)
from ocatari.vision.extract_vision_info import detect_objects_vision
from ocatari.vision.utils import mark_bb, to_rgba
from ocatari.ram.game_objects import GameObject, ValueObject
from ocatari.vision.game_objects import GameObject as GameObjectVision
from ocatari.utils import draw_label, draw_arrow
from gymnasium.error import NameNotFound
import warnings

try:
    # ALE (Arcade Learning Environment) is required for running Atari environments.
    import ale_py
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        '\nALE is required when using the ALE env wrapper. Try `pip install "gymnasium[atari, accept-rom-license]"`\n')


try:
    # OpenCV is used for processing frames for observation (e.g., resizing, grayscaling)
    import cv2
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        '\nOpenCV is required when using the ALE env wrapper. Try `pip install opencv-python`.')

try:
    import pygame  # Pygame is required for rendering the environment for human visualization
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        '\npygame is required for human rendering. Try `pip install pygame`.')

# List of available games for the OCAtari environment
AVAILABLE_GAMES = [
    "Adventure", "AirRaid", "Alien", "Amidar", "Assault", "Asterix", "Asteroids", "Atlantis", "BankHeist", "BattleZone",
    "BeamRider", "Berzerk", "Bowling", "Boxing", "Breakout", "Carnival", "Centipede", "ChopperCommand", "CrazyClimber",
    "DemonAttack", "DonkeyKong", "DoubleDunk", "Enduro", "FishingDerby", "Freeway", "Frogger", "Frostbite", "Galaxian",
    "Gopher", "Hero", "IceHockey", "Jamesbond", "Kangaroo", "KeystoneKapers", "KingKong", "Krull", "KungFuMaster",
    "MarioBros", "MontezumaRevenge", "MsPacman", "NameThisGame", "Pacman", "Phoenix", "Pitfall", "Pitfall2", "Pong",
    "Pooyan", "PrivateEye", "Qbert", "Riverraid", "RoadRunner", "Robotank", "Seaquest", "Skiing", "SpaceInvaders", "StarGunner",
    "Tennis", "TimePilot", "UpNDown", "Venture", "VideoPinball", "YarsRevenge", "Zaxxon"
]

# Constant to control the upscaling factor for rendering
UPSCALE_FACTOR = 6


# The OCAtari environment provides an interface to interact with Atari 2600 games through Gymnasium, enabling object tracking and analysis. This environment extends the functionality of traditional Atari environments by incorporating different object detection modes (RAM, vision, or both) and supports enhanced observation spaces for advanced tasks like reinforcement learning.
class OCAtari(gym.Env):
    """
    :param env_name: The name of the Atari gymnasium environment e.g. "Pong" or "PongNoFrameskip-v5"
    :type env_name: str
    :param mode: The detection method type: one of `raw`, `ram`, `vision`, or `both` (i.e. `ram` + `vision`)
    :type mode: str
    :param hud: Whether to include or not objects from the HUD (e.g. scores, lives)
    :type hud: bool
    :param obs_mode: Define the observation mode. Set to `dqn` (84x84, grayscaled), `ori` (210x160x3, RGB image), `obj` (#Objectsx4). `dqn` and `ori` are also organized in a stack of the last 4 frames.
    :type obs_mode: str
    :param buffer_window_size: The size of the buffer window for observation stacks.
    :type buffer_window_size: int
    :param create_buffer_stacks: Decide what stacks you want to create. The obs_mode automatically add the fitting stack itself. Add "dqn" or "obj" if you want additional stacks.
    :type create_buffer_stacks: list

    The remaining \*args and \**kwargs will be passed to the `gymnasium.make` function.
    """

    def __init__(self, env_name, mode="ram", hud=False, obs_mode="obj", render_mode=None, render_oc_overlay=False, buffer_window_size=4, create_buffer_stacks=["ori"], *args, **kwargs):
        # Determine the game name and check if it's supported
        # Extract the game name and ensure it's within the supported games
        game_name = env_name.split("/")[1].split("-")[0].split("No")[0].split("Deterministic")[
            0] if "ALE/" in env_name else env_name.split("-")[0].split("No")[0].split("Deterministic")[0]
        # if game_name[:4] not in [gn[:4] for gn in AVAILABLE_GAMES]:
        #     raise ValueError(f"Game '{env_name}' not covered yet by OCAtari")

        # Initialization of environment attributes
        # Store the name of the environment and game
        self.env_name = env_name
        self.game_name = game_name
        # Set the mode for object detection (RAM, vision, etc.)
        self.mode = mode
        # Set the observation mode (dqn, obj, ori)
        self.obs_mode = obs_mode
        # Whether to include HUD elements in the object detection
        self.hud = hud
        # Set the render mode for the environment
        gym_render_mode = "rgb_array" if render_oc_overlay else render_mode
        # Set the buffer window size for observations, allowing customization via kwargs
        self.buffer_window_size = buffer_window_size

        # Attempt to create the environment; fallback if necessary
        # Initialize the Atari environment with the specified rendering options
        try:
            self._env = gym.make(
                env_name, render_mode=gym_render_mode, *args, **kwargs)
        except NameNotFound:
            # If the environment name is not found, try using the default ALE naming convention
            cenv_name = f"ALE/{env_name}-v5"
            self._env = gym.make(
                cenv_name, render_mode=gym_render_mode, *args, **kwargs)
            self.env_name = cenv_name

        # Define observation space based on the observation mode
        if obs_mode == "ori":
            pass
        elif obs_mode == "dqn":
            # Set stack for DQN mode (grayscale, 84x84)
            create_buffer_stacks.append("dqn")
            self._env.observation_space = gym.spaces.Box(
                0, 255.0, (self.buffer_window_size, 84, 84))
        elif obs_mode == "obj":
            # Set up object tracking and observation properties
            # Get the maximum number of objects per category for the game
            self.max_objects_per_cat = get_max_objects(
                self.game_name, self.hud)
            # Create a dictionary of game object classes for categorization
            self._class_dict = get_class_dict(self.game_name)
            # Initialize slots to store all possible game objects
            self._slots = [self._class_dict[c]()
                           for c, n in self.max_objects_per_cat.items()
                           for _ in range(n)]
            # Initialize the neurosymbolic state representation with zeros
            self._ns_state = np.zeros(
                sum([len(o._nsrepr) for o in self._slots]))
            # Store the meaning of each neurosymbolic state representation
            self.ns_meaning = [
                f"{o.category} ({o._ns_meaning})" for o in self._slots]
            # Create a stack of ns_states (objects, buffer_size x ocss)
            create_buffer_stacks.append("obj")
            self._env.observation_space = gym.spaces.Box(
                0, 255.0, (self.buffer_window_size, get_object_state_size(self.game_name, self.hud)))
            import warnings
            # warnings.warn("With Release 2.0 we switched to our new object-centric representation, see", DeprecationWarning)
        else:
            raise AttributeError("No valid obs_mode was selected")

        # Set rendering and buffer attributes
        self.render_mode = render_mode
        self.render_oc_overlay = render_oc_overlay
        self.rendering_initialized = False

        # Buffers to store RGB, DQN, and neurosymbolic states
        # Store whether to create specific stacks
        self.create_rgb_stack = "ori" in create_buffer_stacks
        self.create_dqn_stack = "dqn" in create_buffer_stacks
        self.create_ns_stack = "obj" in create_buffer_stacks
        self._state_buffer_rgb = deque(
            [], maxlen=self.buffer_window_size) if self.create_rgb_stack else None
        self._state_buffer_ns = deque(
            [], maxlen=self.buffer_window_size) if self.create_ns_stack else None
        self._state_buffer_dqn = deque(
            [], maxlen=self.buffer_window_size) if self.create_dqn_stack else None
        # Set action space based on the environment's action space
        self.action_space = self._env.action_space
        # Store the ALE interface of the environment
        self._ale = self._env.unwrapped.ale
        self.ale = self._ale

        # Inherit every attribute and method of the base environment
        # Dynamically set attributes of the base Gymnasium environment to this class
        for meth in dir(self._env):
            if meth not in dir(self):
                try:
                    setattr(self, meth, getattr(self._env, meth))
                except AttributeError:
                    pass

        # Set up object detection methods based on mode
        global init_objects
        if mode == "vision":
            # Set object detection to use vision-based extraction
            self.detect_objects = self._detect_objects_vision
            self.objects = init_objects(self.game_name, self.hud, vision=True)
        elif mode in ["ram"]:
            # Set object detection to use RAM-based extraction
            self.detect_objects = self._detect_objects_ram
            self.objects = init_objects(self.game_name, self.hud)
        elif mode == "both":
            # Set object detection to use both RAM and vision-based extraction
            self.detect_objects = self._detect_objects_both
            self.objects_v = init_objects(self.game_name, self.hud)
        else:
            raise ValueError("Undefined mode for information extraction")

    def step(self, *args, **kwargs):
        """
        Run one timestep of the environment's dynamics using the agent actions.
        This function takes an action, steps the environment, and returns the new state, reward, and other information.
        Additionally, it updates object detection based on the configured detection mode and fills observation buffers.

        :param args: Arguments to be passed to the base environment's step function.
        :param kwargs: Keyword arguments to be passed to the base environment's step function.
        :return: A tuple containing:
                 - obs: The observation of the environment after the action, format depends on `obs_mode`.
                 - reward: The reward achieved by the previous action.
                 - truncated: Whether the episode was truncated.
                 - terminated: Whether the episode has ended.
                 - info: Additional information from the environment.
        :rtype: tuple
        """
        # Execute the action and obtain the next state and reward
        obs, reward, terminated, truncated, info = self._env.step(
            *args, **kwargs)
        # Detect objects based on the configured detection mode
        self.detect_objects()
        # Fill the buffer for observations
        self._fill_buffer()
        # Set the observation based on the selected observation mode
        if self.obs_mode == "dqn":
            obs = np.array(self._state_buffer_dqn)
        elif self.obs_mode == "obj":
            obs = np.array(self._state_buffer_ns)
        return obs, reward, truncated, terminated, info

    def _detect_objects_ram(self):
        # Detect objects using RAM-based extraction
        detect_objects_ram(
            self.objects, self._env.env.unwrapped.ale.getRAM(), self.game_name, self.hud)  # type: ignore

    def _detect_objects_vision(self):
        """
        Detect objects using vision-based extraction.

        This method analyzes the RGB screen output of the environment to detect objects visually.
        It is useful when direct access to the RAM state is either unavailable or unsuitable for the desired analysis.
        Vision-based detection allows for tracking in-game elements through computer vision techniques, providing an alternative to RAM-based methods, which rely on specific memory addresses.
        """
        # Detect objects using vision-based extraction
        detect_objects_vision(
            self.objects, self._env.env.unwrapped.ale.getScreenRGB(), self.game_name, self.hud)  # type: ignore

    def _detect_objects_both(self):
        # Use both RAM and vision-based extraction methods to detect objects
        detect_objects_ram(
            self.objects, self._env.env.unwrapped.ale.getRAM(), self.game_name, self.hud)  # type: ignore
        detect_objects_vision(
            self.objects_v, self._env.env.unwrapped.ale.getScreenRGB(), self.game_name, self.hud)  # type: ignore

    def _reset_buffer(self):
        # Reset the buffer by filling it with the initial states
        for _ in range(self.buffer_window_size):
            self._fill_buffer()

    def reset(self, *args, **kwargs):
        """
        Resets the buffer and environment to an initial internal state, returning an initial observation and info.

        This function resets the environment to its initial state, which can be useful when starting a new episode.
        It also reinitializes the buffers that store observations and ensures that object detection is performed.

        :param args: Arguments to be passed to the base environment's reset function.
        :param kwargs: Keyword arguments to be passed to the base environment's reset function.
        :return: A tuple containing:
                 - obs: The initial observation of the environment after the reset.
                 - info: Additional information from the environment.
        :rtype: tuple
        """
        # Reset the environment and detect objects from the initial state
        obs, info = self._env.reset(*args, **kwargs)
        self.objects = init_objects(
            self.game_name, self.hud, vision=self.mode == "vision")
        self.detect_objects()
        # Reset the buffer after environment reset
        self._reset_buffer()
        # Set the observation based on the selected observation mode
        if self.obs_mode == "dqn":
            obs = np.array(self._state_buffer_dqn)
        elif self.obs_mode == "obj":
            obs = np.array(self._state_buffer_ns)
        return obs, info

    def _fill_buffer(self):
        # Fill the RGB, DQN, and neurosymbolic state buffers with the current states
        if self.create_dqn_stack:
            dqn_obs = cv2.resize(cv2.cvtColor(self.getScreenRGB(
            ), cv2.COLOR_RGB2GRAY), (84, 84), interpolation=cv2.INTER_AREA)
            self._state_buffer_dqn.append(dqn_obs)
        if self.create_rgb_stack:
            self._state_buffer_rgb.append(self.getScreenRGB())
        if self.create_ns_stack:
            self._state_buffer_ns.append(self.ns_state)
    window: pygame.Surface = None
    clock: pygame.time.Clock = None

    def _initialize_rendering(self, sample_image):
        # Initialize rendering with Pygame using a sample image to determine size
        assert sample_image is not None
        pygame.init()
        if self.render_mode == "human":
            pygame.display.set_caption(self.game_name)
        self.image_size = (sample_image.shape[1], sample_image.shape[0])
        # render with higher res
        self.window_size = (
            sample_image.shape[1] * UPSCALE_FACTOR, sample_image.shape[0] * UPSCALE_FACTOR)
        self.label_font = pygame.font.SysFont('Pixel12x10', 16)
        if self.render_mode == "human":
            self.window = pygame.display.set_mode(self.window_size)
            self.clock = pygame.time.Clock()
        else:
            self.window = pygame.Surface(self.window_size)
        self.rendering_initialized = True

    def render(self, image=None):
        """
        Compute the render frames (as specified by render_mode during the initialization of the environment).
        If activated, adds an overlay visualizing object properties like position, velocity vector, name, etc.
        """
        # Render the environment image

        if image is None:
            image = self._env.render()

        if not self.render_oc_overlay:
            if self.rendering_initialized:
                # Upscale and return the rendered image
                return image.swapaxes(0, 1).repeat(UPSCALE_FACTOR, axis=0).repeat(UPSCALE_FACTOR, axis=1)
            return image
        if not self.rendering_initialized:
            self._initialize_rendering(image)

        # Prepare the image surface for rendering
        image = np.transpose(image, (1, 0, 2))
        image_surface = pygame.Surface(self.image_size)
        pygame.pixelcopy.array_to_surface(image_surface, image)
        upscaled_image = pygame.transform.scale(
            image_surface, self.window_size)
        self.window.blit(upscaled_image, (0, 0))

        # Overlay surface for additional visualizations like bounding boxes
        overlay_surface = pygame.Surface(self.window_size)
        overlay_surface.set_colorkey((0, 0, 0))

        # Draw detected objects as bounding boxes with labels
        for game_object in self.objects:
            x, y = game_object.xy
            w, h = game_object.wh

            if x == np.nan:
                continue

            # Scale object properties for rendering
            dx, dy = game_object.dx * UPSCALE_FACTOR, game_object.dy * UPSCALE_FACTOR
            x, y, w, h = x * UPSCALE_FACTOR, y * UPSCALE_FACTOR, w * \
                UPSCALE_FACTOR, h * UPSCALE_FACTOR
            x_c, y_c = x + w // 2, y + h // 2

            # Draw bounding box
            pygame.draw.rect(
                overlay_surface, color=game_object.rgb, rect=(x, y, w, h), width=2)
            # Draw label with object category
            label = game_object.category
            if isinstance(game_object, ValueObject):
                label += f" ({game_object.value})"
            draw_label(self.window, label, position=(
                x, y + h + 4), font=self.label_font)
            # Draw velocity vector if applicable
            if dx != 0 or dy != 0:
                draw_arrow(overlay_surface, start_pos=(float(x_c), float(y_c)), end_pos=(
                    x_c + 2 * dx, y_c + 2 * dy), color=(100, 200, 255), width=2)

        self.window.blit(overlay_surface, (0, 0))

        # Update the display for human rendering or return the image array for rgb_array mode
        if self.render_mode == "human":
            frameskip = self._env.unwrapped._frameskip if isinstance(
                self._env.unwrapped._frameskip, int) else 1
            self.clock.tick(60 // frameskip)
            pygame.display.flip()
            pygame.event.pump()
        elif self.render_mode == "rgb_array":
            return pygame.surfarray.array3d(self.window)

    def close(self, *args, **kwargs):
        """
        Close the environment and perform cleanup.
        """
        return self._env.close(*args, **kwargs)

    def seed(self, seed, *args, **kwargs):
        # Set the random seed for reproducibility
        self._env.seed(seed, *args, **kwargs)

    def getScreenRGB(self):
        """
        Returns the current RGB screen state of the environment.

        :return: A NumPy array representing the RGB screen state.
        :rtype: np.array
        """
        return self._ale.getScreenRGB()

    @property
    def nb_actions(self):
        """
        The number of actions available in this environment.
        """
        return self.action_space.n

    @property
    def get_rgb_state(self):
        """
        Returns the current RGB state of the environment.
        """
        return self._ale.getScreenRGB()

    def set_ram(self, target_ram_position, new_value):
        """
        Directly set a given value at a targeted RAM position.
        """
        return self._env.unwrapped.ale.setRAM(target_ram_position, new_value)

    def get_ram(self):
        """
        Returns the RAM state.
        """
        return self._ale.getRAM()

    def get_action_meanings(self):
        # Return the meanings of each action
        return self._env.env.env.get_action_meanings()

    def _get_obs(self):
        # Get the current observation from the environment
        return self._env.env.env.unwrapped._get_obs()

    def detect_objects_both(self):
        # Use both RAM and vision-based methods to detect objects
        self._detect_objects_ram()
        self._detect_objects_vision()

    def _clone_state(self):
        """
        Returns the current system state of the environment.
        """
        return self._env.env.env.ale.cloneSystemState()

    def _restore_state(self, state):
        """
        Restore the system state of the environment.
        """
        return self._env.env.env.ale.restoreSystemState(state)

    @property
    def ns_state(self):
        """
        Returns the current neurosymbolic state of the environment.
        """
        return list(chain.from_iterable([o._nsrepr for o in self.objects]))

    def render_explanations(self):
        # Render explanations by highlighting the objects with bounding boxes
        rendered = np.zeros_like(self._state_buffer_rgb[0]).astype(float)
        coefs = [0.05, 0.1, 0.25, 0.6]
        for coef, state_i in zip(coefs, self._state_buffer_rgb):
            rendered += coef * state_i
        rendered = rendered.astype(int)
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
        t_height = 0.03 * len(rows)
        table = plt.table(cellText=cells, rowLabels=rows, rowColours=colors, colLabels=columns,
                          colWidths=[.2, .2, .3], bbox=[0.1, 1.02, 0.8, t_height], loc='top')
        table.set_fontsize(14)
        plt.subplots_adjust(top=0.8)
        plt.show()

    def aggregated_render(self, coefs=[0.05, 0.1, 0.25, 0.6]):
        # Generate a weighted sum of frames for a more informative representation
        rendered = np.zeros_like(self._state_buffer_rgb[0]).astype(float)
        for coef, state_i in zip(coefs, self._state_buffer_rgb):
            rendered += coef * state_i
        rendered = rendered.astype(int)
        return rendered

    def get_keys_to_action(self):
        return self._env.unwrapped.get_keys_to_action()
