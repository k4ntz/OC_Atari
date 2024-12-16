"""
This script is used to simply play the Atari games manually.
"""
import imageio
import gymnasium as gym
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
import pygame
from ocatari.core import OCAtari
import os
from argparse import ArgumentParser
import cv2


parser = ArgumentParser()
parser.add_argument("-g", "--game", type=str, default="Pong")
parser.add_argument("-r", "--record", action="store_true")
parser.add_argument("-pr", "--print-reward", action="store_true")

args = parser.parse_args()


def save_rgb_array_as_png(rgb_array, filename):
    imageio.imwrite(filename, rgb_array)


def save_patch_as_png(patch, filename):
    (filename, patch)


def retrieve_objects_patch(object, frame, zoom=20):
    x, y, w, h = object.xywh
    patch = frame[y:y+h, x:x+w]
    patch = np.repeat(np.repeat(patch, zoom, axis=0), zoom, axis=1)
    patch_rgba = cv2.cvtColor(patch, cv2.COLOR_BGR2BGRA)

    # Step 3: Remove the background
    # Set the alpha channel to 0 (transparent) where the color doesn't match the object RGB
    for i in range(h*zoom):
        for j in range(w*zoom):
            # Get the pixel color at (i, j)
            pixel_color = patch_rgba[i, j][:3]  # RGB part
            # Compare it to the object RGB color
            if not np.all(pixel_color == object.rgb):
                # Set alpha to 0 if it doesn't match the object's RGB
                patch_rgba[i, j][3] = 0  # Set alpha to 0 (transparent)
            else:
                # Keep the alpha to 255 (opaque) if it matches
                patch_rgba[i, j][3] = 255
    return patch_rgba


def save_objects_patches(objects, frame, game):
    for object in objects:
        patch = retrieve_objects_patch(object, frame)
        if not os.path.isdir(f'patches/{game}'):
            os.makedirs(f'patches/{game}', exist_ok=True)
        i = 0
        while os.path.exists(f'patches/{game}/{object.category}_{i}.png'):
            i += 1
        imageio.imwrite(f'patches/{game}/{object.category}_{i}.png', patch)
    print(f"Objects patches saved in patches/{game}")


class Renderer:
    env: gym.Env

    def __init__(self, env_name: str):
        self.env = OCAtari(env_name, mode="vision", hud=True, render_mode="human",
                           render_oc_overlay=True, frameskip=1)
        self.env.reset()
        self.env.render()  # initialize pygame video system

        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()
        self.frame = 0
        self.env.set_ram(16, 6)

    def run(self):
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                obs, reward, term, trunc, info = self.env.step(action)
                self.env.render()
                if args.record and self.frame % 4 == 0:
                    frame = self.env.unwrapped.ale.getScreenRGB()
                    save_rgb_array_as_png(
                        frame, f'frames/{args.game}_{self.frame}.png')
                if args.print_reward and reward != 0:
                    print(reward)
                self.frame += 1
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

                if event.key == pygame.K_o:  # 'O': Save objects
                    screen = self.env.unwrapped.ale.getScreenRGB()
                    save_objects_patches(
                        self.env.objects, screen, self.env.game_name)
                    screen = np.repeat(np.repeat(screen, 6, axis=0), 6, axis=1)
                    save_rgb_array_as_png(
                        screen, f'patches/{self.env.game_name}_{self.frame}.png')

                elif (event.key,) in self.keys2actions.keys():  # env action
                    self.current_keys_down.add(event.key)

            elif event.type == pygame.KEYUP:  # keyboard key released
                if (event.key,) in self.keys2actions.keys():
                    self.current_keys_down.remove(event.key)


if __name__ == "__main__":
    # renderer = Renderer(args.game)
    # renderer = Renderer("Seaquest")
    renderer = Renderer(args.game)
    renderer.run()
