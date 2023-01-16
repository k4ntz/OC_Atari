import gym
from ram.extract_ram_info import augment_info_raw, augment_info_revised
from vision.extract_vision_info import augment_info_vision
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

AVAILABLE_GAMES = ["Boxing", "Breakout", "Skiing", "Pong", "Seaquest",
                   "Skiing", "SpaceInvaders", "Tennis", "Freeway", "MsPacman"]


class OCAtari():
    def __init__(self, env_name, mode="raw", *args, **kwargs):
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
        if mode == "vision":
            self.augment_info = augment_info_vision
            self.step = self._step_vision
        elif mode == "raw":
            self.augment_info = augment_info_raw
            self.step = self._step_ram
        elif mode == "revised":
            self.augment_info = augment_info_revised
            self.step = self._step_ram
        else:
            print(colored("Undefined mode for information extraction", "red"))
            exit(1)
        self.window = 4
        self._state_buffer = deque([], maxlen=self.window)
        self.action_space = self._env.action_space

    def _step_ram(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        self.augment_info(info, self._env.env.unwrapped.ale.getRAM(), self.game_name)
        self._fill_buffer()
        return obs, reward, truncated, terminated, info

    def _step_vision(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        self.augment_info(info, obs, self.game_name)
        self._fill_buffer()
        return obs, reward, truncated, terminated, info

    def _reset_buffer(self):
        for _ in range(self.window):
            self._state_buffer.append(
                torch.zeros(84, 84, device=DEVICE, dtype=torch.uint8)
            )

    def reset(self, *args, **kwargs):
        self._reset_buffer()
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

    @property
    def dqn_obs(self):
        return torch.stack(list(self._state_buffer), 0).unsqueeze(0).byte()
