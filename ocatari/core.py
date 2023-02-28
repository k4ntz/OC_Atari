import gymnasium as gym
from ocatari.ram.extract_ram_info import detect_objects_raw, detect_objects_revised, init_objects
from ocatari.vision.extract_vision_info import detect_objects_vision
from termcolor import colored
from collections import deque
try:
    import cv2
except ModuleNotFoundError:
    print(
        "\nOpenCV is required when using the ALE env wrapper. ",
        "Try `pip install opencv-python`.\n",
    )
import torch

DEVICE = "cpu"


<<<<<<< HEAD
AVAILABLE_GAMES = ["Asterix", "Boxing", "Breakout", "Skiing", "Pong", "Seaquest",
                   "Skiing", "SpaceInvaders", "Tennis", "Freeway", "DemonAttack", "Bowling",
                   "MsPacman", "Kangaroo", "Berzerk", "Carnival", "Centipede"]

=======
AVAILABLE_GAMES = ["Asterix", "Berzerk", "Bowling", "Boxing", "Breakout", "Carnival", "DemonAttack", 
                   "Freeway", "Kangaroo", "MsPacman", "Pong", "Seaquest", "Skiing", "SpaceInvaders", 
                   "Tennis"]
>>>>>>> 051d87cdc9ca1d362a4c11382d9100313d43e259

class OCAtari:
    def __init__(self, env_name, mode="raw", hud=False, *args, **kwargs):
        """
        mode: raw/revised/vision/both
        """
        if env_name[:4] not in [gn[:4] for gn in AVAILABLE_GAMES]:
            print(colored("Game not available in OCAtari", "red"))
            print("Available games: ", AVAILABLE_GAMES)
            exit(1)
        self._env = gym.make(env_name, *args, **kwargs)
        self.game_name = env_name.split("-")[0].split("No")[0].split("Deterministic")[0]
        self.mode = mode
        self._ale = self._env.unwrapped.ale
        self.hud = hud
        self.objects = init_objects(self.game_name, self.hud)
        if mode == "vision":
            self.detect_objects = detect_objects_vision
            self.step = self._step_vision
        elif mode == "raw":
            self.detect_objects = detect_objects_raw
            self.step = self._step_ram
        elif mode == "revised":
            self.detect_objects = detect_objects_revised
            self.step = self._step_ram
        elif mode == "test":
            self.detect_objects_v = detect_objects_vision
            self.detect_objects_r = detect_objects_revised
            self.objects_v = init_objects(self.game_name, self.hud)
            self.step = self._step_test
        else:
            print(colored("Undefined mode for information extraction", "red"))
            exit(1)
        self.window = 4
        self._state_buffer = deque([], maxlen=self.window)
        self.action_space = self._env.action_space

    def _step_ram(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        self.detect_objects(self.objects, self._env.env.unwrapped.ale.getRAM(), self.game_name, self.hud)
        self._fill_buffer()
        return obs, reward, truncated, terminated, info

    def _step_vision(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        self.detect_objects(self.objects, obs, self.game_name, self.hud)
        self._fill_buffer()
        return obs, reward, truncated, terminated, info

    def _step_test(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        self.detect_objects_r(self.objects, self._env.env.unwrapped.ale.getRAM(), self.game_name, self.hud)
        self.detect_objects_v(self.objects_v, obs, self.game_name, self.hud)
        self._fill_buffer()
        return obs, reward, truncated, terminated, info

    def _reset_buffer(self):
        for _ in range(self.window):
            self._state_buffer.append(
                torch.zeros(84, 84, device=DEVICE, dtype=torch.uint8)
            )

    def reset(self, *args, **kwargs):
        self._reset_buffer()
        self.objects = init_objects(self.game_name, self.hud)
        return self._env.reset(*args, **kwargs)

    def _fill_buffer(self):
        state = cv2.resize(
            self._ale.getScreenGrayscale(), (84, 84), interpolation=cv2.INTER_AREA,
        )
        self._state_buffer.append(torch.tensor(state, dtype=torch.uint8,
                                               device=DEVICE))

    def render(self, *args, **kwargs):
        return self._env.render(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self._env.close(*args, **kwargs)
    
    def seed(self, seed, *args, **kwargs):
        self._env.seed(seed, *args, **kwargs)

    @property
    def nb_actions(self):
        return self._env.unwrapped.action_space.n

    @property
    def dqn_obs(self):
        return torch.stack(list(self._state_buffer), 0).unsqueeze(0).byte()

    def set_ram(self, target_ram_position, new_value):
        """
        Directly manipulate a targeted RAM position
        """
        return self._env.unwrapped.ale.setRAM(target_ram_position, new_value)
