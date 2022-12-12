import gym
from extract_ram_info import augment_info_raw, augment_info_revised
from extract_vision_info import augment_info_vision
from termcolor import colored


AVAILABLE_GAMES = ["Boxing", "Breakout", "Skiing", "Pong", "Seaquest", "Tennis"]


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

    def _step_ram(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        self.augment_info(info, self._env.env.unwrapped.ale.getRAM(), self.game_name)
        return obs, reward, truncated, terminated, info

    def _step_vision(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        self.augment_info(info, obs, self.game_name)
        return obs, reward, truncated, terminated, info

    def reset(self, *args, **kwargs):
        return self._env.reset(*args, **kwargs)

    def render(self, *args, **kwargs):
        return self._env.render(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self._env.close(*args, **kwargs)
