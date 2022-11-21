import gym
from termcolor import colored
from extract_ram_info import augment_info


AVAILABLE_GAMES = ["Breakout", "Skiing"]

class OCAtari():
    def __init__(self, env_name):
        if env_name[:4] not in [gn[:4] for gn in AVAILABLE_GAMES]:
            print(colored("Game not available in OCAtari", "red"))
            print("Available games: ", AVAILABLE_GAMES)
            exit(1)
        self._env = gym.make(env_name, render_mode="human")
        self.game_name = env_name.split("-")[0].split("No")[0].split("Deterministic")[0]

    def step(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        augment_info(info, self._env.env.unwrapped.ale.getRAM(), self.game_name)
        return obs, reward, truncated, terminated, info

    def reset(self, *args, **kwargs):
        return self._env.reset(*args, **kwargs)

    def render(self, *args, **kwargs):
        return self._env.render(*args, **kwargs)
