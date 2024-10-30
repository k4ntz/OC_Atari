"""
This script is used to simply play the Atari games manually.
"""
import gymnasium as gym
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
import pygame
from ocatari.core import OCAtari
from copy import deepcopy as copy
from argparse import ArgumentParser
import random 
import os, pickle

parser = ArgumentParser()
parser.add_argument("-g", "--game", type=str, default="Pong")
parser.add_argument("-pr", "--print-reward", action="store_true")
parser.add_argument("-n", "--number_samples", type=int, default=1000)

args = parser.parse_args()

import imageio

def save_rgb_array_as_png(rgb_array, filename):
    imageio.imwrite(filename, rgb_array)

class Renderer:
    env: gym.Env

    def __init__(self, env_name: str):
        env_name = f"{env_name}NoFrameskip-v4"
        self.env = OCAtari(env_name, mode="ram", hud=True, render_mode="human",
                           render_oc_overlay=True, frameskip=1)
        self.env.reset()
        self.env.render()  # initialize pygame video system

        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()
        self.frame = 0
        self.record = False
        self.buffer = []
        self.last_ram = None
        self._gen_action_conversion()
        
    def _gen_action_conversion(self):
        actions = self.env.unwrapped.get_action_meanings()
        self.act_conv = []
        for i, action in enumerate(actions):
            act_tuple = [0, 0, 0] # x_axis, y_axis, button
            if "FIRE" in action:
                act_tuple[2] = 1
            if "LEFT" in action:
                act_tuple[0] = -1
            elif "RIGHT" in action:
                act_tuple[0] = 1
            if "DOWN" in action:
                act_tuple[1] = -1
            elif "UP" in action:
                act_tuple[1] = +1
            self.act_conv.append(tuple(act_tuple))

    def run(self):
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                obs, reward, term, trunc, info = self.env.step(action)
                current_ram = self.env.unwrapped.ale.getRAM()
                self.env.render()
                if self.last_ram is not None and self.record and random.random() < 0.1:
                    self.buffer.append((self.last_ram, self.act_conv[action], current_ram))
                self.last_ram = copy(current_ram)
                self.frame += 1
            if len(self.buffer) >= args.number_samples:
                os.makedirs("transitions", exist_ok=True)
                pickle.dump(self.buffer, open(f"transitions/{args.game}_data.pkl", "wb"))
                self.running = False
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
                
                if event.key == pygame.K_m:  # 'm': start recording
                    self.record = True
                    print("\n\nRecording started\n\n")

                elif (event.key,) in self.keys2actions.keys():  # env action
                    self.current_keys_down.add(event.key)

            elif event.type == pygame.KEYUP:  # keyboard key released
                if (event.key,) in self.keys2actions.keys():
                    self.current_keys_down.remove(event.key)


if __name__ == "__main__":
    renderer = Renderer(args.game)
    renderer.run()
