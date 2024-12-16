import gymnasium as gym
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
import pygame
from ocatari.core import OCAtari, UPSCALE_FACTOR
from gymnasium.error import NameNotFound
import pickle
"""
This script can be used to identify any RAM positions that
influence the color of a specific pixel. This can be used to
identify the values that belong to a GameObject.
"""


import pygame
from ocatari.core import OCAtari, DEVICE, EasyDonkey
import numpy as np
import torch
import cv2
import random


def get_bin(x): return format(x, 'b').zfill(8)


RAM_RENDER_WIDTH = 1000
RAM_N_COLS = 8
RAM_CELL_WIDTH = 115
RAM_CELL_HEIGHT = 45


class Renderer:
    window: pygame.Surface
    clock: pygame.time.Clock
    env: gym.Env

    def __init__(self, env_name: str):
        try:
            self.env = OCAtari(env_name, mode="ram", hud=True, render_mode="rgb_array",
                               render_oc_overlay=True, frameskip=1)
        except NameNotFound:
            self.env = gym.make(env_name, render_mode="rgb_array", frameskip=1)
        self.env.reset(seed=42)[0]
        self.current_frame = self.env.render()
        self._init_pygame(self.current_frame)
        self.paused = False

        self.current_keys_down = set()
        self.current_mouse_pos = None
        self.keys2actions = self.env.unwrapped.get_keys_to_action()

        self.ram_grid_anchor_left = self.env_render_shape[0] + 28
        self.ram_grid_anchor_top = 28

        self.active_cell_idx = None
        self.candidate_cell_ids = []
        self.current_active_cell_input: str = ""

    def _init_pygame(self, sample_image):
        pygame.init()
        pygame.display.set_caption("OCAtari Environment")
        self.env_render_shape = sample_image.shape[:2]
        window_size = (self.env_render_shape[0], self.env_render_shape[1])
        self.window = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()

    def run(self):
        self.running = True
        while self.running:
            self._handle_user_input()
            ram = self.env.unwrapped.ale.getRAM()
            if not self.paused:
                action = self._get_action()
                tuple = self.env.step(action)
                rew = tuple[1]
                if rew != 0:
                    print(rew)
                self.current_frame = self.env.render().copy()
            self._render()
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

                elif event.key == pygame.K_r:  # 'R': reset
                    self.env.reset()

                elif event.key == pygame.K_m:  # 'M': save snapshot
                    snapshot = self.env._ale.cloneState()
                    pickle.dump(snapshot, open("snapshot.pkl", "wb"))
                    print("Saved snapshot.pkl")

                elif event.key == pygame.K_ESCAPE and self.active_cell_idx is not None:
                    self._unselect_active_cell()

                elif (event.key,) in self.keys2actions.keys():  # env action
                    self.current_keys_down.add(event.key)

                elif pygame.K_0 <= event.key <= pygame.K_9:  # enter digit
                    char = str(event.key - pygame.K_0)
                    if self.active_cell_idx is not None:
                        self.current_active_cell_input += char

                elif event.key == pygame.K_BACKSPACE:  # remove character
                    if self.active_cell_idx is not None:
                        self.current_active_cell_input = self.current_active_cell_input[:-1]

                elif event.key == pygame.K_RETURN:
                    if self.active_cell_idx is not None:
                        if len(self.current_active_cell_input) > 0:
                            new_cell_value = int(
                                self.current_active_cell_input)
                            if new_cell_value < 256:
                                self._set_ram_value_at(
                                    self.active_cell_idx, new_cell_value)
                        self._unselect_active_cell()

            elif event.type == pygame.KEYUP:  # keyboard key released
                if (event.key,) in self.keys2actions.keys():
                    self.current_keys_down.remove(event.key)

    def _render(self, frame=None):
        self.window.fill((0, 0, 0))  # clear the entire window
        self._render_atari(frame)
        pygame.display.flip()
        pygame.event.pump()

    def _render_atari(self, frame=None):
        if frame is None:
            frame = self.current_frame
        frame_surface = pygame.Surface(self.env_render_shape)
        pygame.pixelcopy.array_to_surface(frame_surface, frame)
        self.window.blit(frame_surface, (0, 0))
        self.clock.tick(60)


if __name__ == "__main__":
    # renderer = Renderer("Pong")
    # renderer = Renderer("DemonAttack")
    # renderer = Renderer("ALE/Pacman-v5")
    # renderer = Renderer("ALE/DonkeyKong-v5")
    # renderer = Renderer("ALE/MontezumaRevenge-v5")
    # renderer = Renderer("Freeway-v4")
    renderer = Renderer("MsPacman-v4")
    # renderer = Renderer("Skiing-v4")
    # renderer = Renderer("Boxing-v4")
    renderer.run()
