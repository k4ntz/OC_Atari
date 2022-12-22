import gym
from ram.extract_ram_info import augment_info_raw, augment_info_revised
from vision.extract_vision_info import augment_info_vision
from termcolor import colored
from vision.utils import mark_bb, make_darker
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

AVAILABLE_GAMES = ["Boxing", "Breakout", "Skiing", "Pong", "Seaquest", "Tennis", "Freeway"]


class OCAtari():
    def __init__(self, env_name, mode="raw", render_mode="human", *args, **kwargs):
        """
        mode: raw/revised/vision/both
        """
        if env_name[:4] not in [gn[:4] for gn in AVAILABLE_GAMES]:
            print(colored("Game not available in OCAtari", "red"))
            print("Available games: ", AVAILABLE_GAMES)
            exit(1)
        self.render_mode = render_mode
        if render_mode == "rgb_array_with_bbs":
            if mode == "raw":
                print(colored("render_mode_with_bbs only works with revised or vision mode", "red"))
            render_mode = 'rgb_array'
        self._env = gym.make(env_name, render_mode=render_mode, *args, **kwargs)
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
        if self.mode == "revised" and self.render_mode == 'rgb_array_with_bbs':
            self.info = info  # for render()
            obs = self._add_bbs(obs, info)
        self._fill_buffer()
        return obs, reward, truncated, terminated, info

    def _step_vision(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        self.augment_info(info, obs, self.game_name)
        if self.render_mode == 'rgb_array_with_bbs':
            self.info = info  # for render()
            obs = self._add_bbs(obs, info)
        self._fill_buffer()
        return obs, reward, truncated, terminated, info

    def _add_bbs(self, obs, info):
        for obj_name, oinfo in info["objects"].items():
            opos = oinfo[:4]
            ocol = oinfo[4:]

            sur_col = make_darker(ocol)
            mark_bb(obs, opos, color=sur_col)
        return obs

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
        obs = self._env.render(*args, **kwargs)
        if (self.mode == "revised" or self.mode == "vision") and \
                self.render_mode == 'rgb_array_with_bbs' and self.info is not None:
            obs = self._add_bbs(obs, self.info)
        return obs

    def close(self, *args, **kwargs):
        return self._env.close(*args, **kwargs)

    @property
    def dqn_obs(self):
        return torch.stack(list(self._state_buffer), 0).unsqueeze(0).byte()
