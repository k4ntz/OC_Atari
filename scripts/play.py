import gymnasium as gym
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
import pygame
from ocatari.core import OCAtari

"""
This script is used to simply play the Atari games manually.
"""


class Renderer:
    env: gym.Env

    def __init__(self, env_name: str):
        self.env = OCAtari(env_name, mode="revised", hud=True, render_mode="human",
                           render_oc_overlay=True, frameskip=1)
        self.env.reset()
        self.env.render()  # initialize pygame video system

        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()
        print(self.keys2actions)

    def run(self):
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                self.env.step(action)
                self.env.render()
        pygame.quit()

    def _get_action(self):
        pressed_keys = list(self.current_keys_down)
        pressed_keys.sort()
        pressed_keys = tuple(pressed_keys)
        if pressed_keys in self.keys2actions.keys():
            return self.keys2actions[pressed_keys]
        else:
            return 0  # NOOP

    def _handle_user_input(self):
        self.current_mouse_pos = np.asarray(pygame.mouse.get_pos())

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:  # window close button clicked
                self.running = False

            elif event.type == pygame.KEYDOWN:  # keyboard key pressed
                if event.key == pygame.K_p:  # 'P': pause/resume
                    self.paused = not self.paused

                if event.key == pygame.K_r:  # 'R': reset
                    self.env.reset()

                elif (event.key,) in self.keys2actions.keys():  # env action
                    self.current_keys_down.add(event.key)

            elif event.type == pygame.KEYUP:  # keyboard key released
                if (event.key,) in self.keys2actions.keys():
                    self.current_keys_down.remove(event.key)


if __name__ == "__main__":
    # renderer = Renderer("Seaquest")
    renderer = Renderer("ALE/DonkeyKong-v5")
    renderer.run()
