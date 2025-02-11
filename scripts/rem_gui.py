import numpy as np
import pygame
from ocatari.core import OCAtari, UPSCALE_FACTOR
from tqdm import tqdm
from collections import deque
from copy import deepcopy
import pickle as pkl
import os
import atexit
from ale_py import Action
import matplotlib.pyplot as plt

"""
This script can be used to identify any RAM positions that
influence the color of a specific pixel. This can be used to
identify the values that belong to a GameObject.
"""

RAM_RENDER_WIDTH = round(1000 * (UPSCALE_FACTOR / 4))
RAM_N_COLS = 8
RAM_CELL_WIDTH = round(115 * (UPSCALE_FACTOR / 4))
RAM_CELL_HEIGHT = round(45 * (UPSCALE_FACTOR / 4))


class Renderer:
    window: pygame.Surface
    clock: pygame.time.Clock
    env: OCAtari

    def __init__(self, env_name, mode='ram', no_render=[]):
        self.env = OCAtari(env_name, mode=mode, hud=True, render_mode="rgb_array",
                           render_oc_overlay=True, frameskip=1, obs_mode="obj", repeat_action_probability=0)

        self.env.reset(seed=42)
        self.current_frame = self.env.render()
        self._init_pygame(self.current_frame)
        self.paused = False

        self.current_keys_down = set()
        self.current_mouse_pos = None
        self.keys2actions = self.env.unwrapped.get_keys_to_action()

        self.ram_grid_anchor_left = self.env_render_shape[0] + round(
            28 * (UPSCALE_FACTOR / 4))
        self.ram_grid_anchor_top = round(28 * (UPSCALE_FACTOR / 4))

        self.active_cell_idx = None
        self.candidate_cell_ids = []
        self.current_active_cell_input: str = ""
        self.no_render = no_render
        self.red_render = []

        self.saved_frames = deque(maxlen=200)  # tuples of ram, state, image
        self.frame_by_frame = False
        self.next_frame = False

    def _init_pygame(self, sample_image):
        pygame.init()
        pygame.display.set_caption("OCAtari Environment")
        self.env_render_shape = sample_image.shape[:2]
        window_size = (
            self.env_render_shape[0] + RAM_RENDER_WIDTH, self.env_render_shape[1])
        self.window = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.ram_cell_id_font = pygame.font.SysFont(
            'Pixel12x10', round(25 * (UPSCALE_FACTOR / 4)))
        self.ram_cell_value_font = pygame.font.SysFont(
            'Pixel12x10', round(30 * (UPSCALE_FACTOR / 4)))

    def run(self):
        self.running = True
        i = 0
        previous_x = 146
        while self.running:
            self._handle_user_input()
            if not (self.frame_by_frame and not (self.next_frame)) and not self.paused:
                self.saved_frames.append((deepcopy(self.env.get_ram()), self.env._ale.cloneState(
                ), self.current_frame))  # ram, state, image (rgb)
                action = self._get_action()
                # self.paddle.step(action.name)
                action = self.env.get_action_meanings().index(action.name)
                reward = self.env.step(action)[1]
                # print(self.paddle.position, self.env.get_ram()[72])
                # print(self.paddle.speed, previous_x - self.env.get_ram()[72])
                previous_x = self.env.get_ram()[72]
                # if reward != 0:
                #     print(reward)
                #     pass
                # self.env.set_ram(59, 105)
                # js = [2, 6, 12, 36, 66, 128, 172]
                # for i, j in zip(range(28, 34), js):
                #     self.env.set_ram(i, 1+j)
                # print(self.env.get_ram()[72])
                self.current_frame = self.env.render().copy()
                self._render()
                self.next_frame = False
            self._render()

            # if i % 300 == 0:
            #     import ipdb; ipdb.set_trace()
            i += 1
        pygame.quit()

    def _get_action(self) -> Action:
        pressed_keys = list(self.current_keys_down)
        pressed_keys.sort()
        pressed_keys = tuple(pressed_keys)
        if pressed_keys in self.keys2actions.keys():
            return self.keys2actions[pressed_keys]
        else:
            return Action.NOOP

    def _handle_user_input(self):
        self.current_mouse_pos = np.asarray(pygame.mouse.get_pos())

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:  # window close button clicked
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button pressed
                    x = self.current_mouse_pos[0] // UPSCALE_FACTOR
                    y = self.current_mouse_pos[1] // UPSCALE_FACTOR
                    if x < 160:
                        self.find_causative_ram(x, y)
                    else:
                        self.active_cell_idx = self._get_cell_under_mouse()
                        self.current_active_cell_input = ""
                elif event.button == 3:  # right mouse button pressed
                    to_hide = self._get_cell_under_mouse()
                    if to_hide in self.no_render:
                        self.no_render.remove(to_hide)
                    else:
                        self.no_render.append(to_hide)
                elif event.button == 2:  # middle mouse button pressed
                    toggle = self._get_cell_under_mouse()
                    if toggle in self.red_render:
                        self.red_render.remove(toggle)
                    else:
                        self.red_render.append(toggle)
                elif event.button == 4:  # mousewheel up
                    cell_idx = self._get_cell_under_mouse()
                    if cell_idx is not None:
                        self._increment_ram_value_at(cell_idx)
                elif event.button == 5:  # mousewheel down
                    cell_idx = self._get_cell_under_mouse()
                    if cell_idx is not None:
                        self._decrement_ram_value_at(cell_idx)

            elif event.type == pygame.KEYDOWN:  # keyboard key pressed
                if event.key == pygame.K_p:  # 'P': pause/resume
                    self.paused = not self.paused

                elif event.key == pygame.K_f:  # Frame by frame
                    self.frame_by_frame = not (self.frame_by_frame)
                    self.next_frame = False

                elif event.key == pygame.K_o:  # 'O': Objects
                    print(self.env.objects)

                elif event.key == pygame.K_n:  # next
                    print("next \n\n")
                    self.next_frame = True

                elif event.key == pygame.K_b:  # 'B': Backwards
                    if self.frame_by_frame:
                        if len(self.saved_frames) > 0:
                            previous = self.saved_frames.pop()
                            for i, ram_v in enumerate(previous[0]):
                                self.env.set_ram(i, ram_v)
                            for i, value in enumerate(previous[0]):
                                self._render_ram_cell(i, value)
                            self.env._ale.restoreState(
                                previous[1])  # restore state
                            self.current_frame = previous[2].copy()
                            self._render_atari()
                            pygame.display.flip()
                            pygame.event.pump()
                        else:
                            print(
                                "There are no prior frames saved to go back to. Save more using the flag --previous_frames")

                if event.key == pygame.K_r:  # 'R': reset
                    self.env.reset()

                if event.key == pygame.K_c:  # 'C': clone
                    if self.paused:
                        statepkl = self.env._ale.cloneState()
                        filename = f"state_{self.env.game_name}.pkl"
                        i = 1
                        while os.path.exists(filename):
                            filename = f"state_{self.env.game_name}_{i}.pkl"
                            i += 1
                        with open(filename, "wb") as f:
                            pkl.dump((statepkl, self.env.objects), f)
                            print(f"State cloned in {filename}")

                if event.key == pygame.K_m:  # 'S': save
                    plt.imshow(self.env._ale.getScreenRGB())
                    plt.show()

                elif event.key == pygame.K_ESCAPE and self.active_cell_idx is not None:
                    self._unselect_active_cell()

                # (event.key,) in self.keys2actions.keys() or [x for x in self.keys2actions.keys() if event.key in x]:  # env action
                elif [x for x in self.keys2actions.keys() if event.key in x]:
                    self.current_keys_down.add(event.key)

                elif pygame.K_0 <= event.key <= pygame.K_9:  # enter digit
                    char = str(event.key - pygame.K_0)
                    if self.active_cell_idx is not None:
                        self.current_active_cell_input += char

                elif pygame.K_KP1 <= event.key <= pygame.K_KP0:  # enter digit
                    char = str((event.key - pygame.K_KP1 + 1) % 10)
                    if self.active_cell_idx is not None:
                        self.current_active_cell_input += char

                elif event.key == pygame.K_BACKSPACE:  # remove character
                    if self.active_cell_idx is not None:
                        self.current_active_cell_input = self.current_active_cell_input[:-1]

                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if self.active_cell_idx is not None:
                        if len(self.current_active_cell_input) > 0:
                            new_cell_value = int(
                                self.current_active_cell_input)
                            if new_cell_value < 256:
                                self._set_ram_value_at(
                                    self.active_cell_idx, new_cell_value)
                        self._unselect_active_cell()

            elif event.type == pygame.KEYUP:  # keyboard key released
                # (event.key,) in self.keys2actions.keys():
                if [x for x in self.keys2actions.keys() if event.key in x]:
                    self.current_keys_down.remove(event.key)

    def _render(self, frame=None):
        self.window.fill((0, 0, 0))  # clear the entire window
        self._render_atari(frame)
        self._render_ram()
        self._render_hover()
        pygame.display.flip()
        pygame.event.pump()

    def _render_atari(self, frame=None):
        if frame is None:
            frame = self.current_frame
        frame_surface = pygame.Surface(self.env_render_shape)
        pygame.pixelcopy.array_to_surface(frame_surface, frame)
        self.window.blit(frame_surface, (0, 0))
        self.clock.tick(60)

    def _render_ram(self):
        ale = self.env.unwrapped.ale
        ram = ale.getRAM()

        for i, value in enumerate(ram):
            self._render_ram_cell(i, value)

    def _get_ram_value_at(self, idx: int):
        ale = self.env.unwrapped.ale
        ram = ale.getRAM()
        return ram[idx]

    def _set_ram_value_at(self, idx: int, value: int):
        ale = self.env.unwrapped.ale
        ale.setRAM(idx, value)
        # self.current_frame = self.env.render()
        # self._render()

    def _set_ram(self, values):
        ale = self.env.unwrapped.ale
        for k, value in enumerate(values):
            ale.setRAM(k, value)

    def _increment_ram_value_at(self, idx: int):
        value = self._get_ram_value_at(idx)
        self._set_ram_value_at(idx, min(value + 1, 255))

    def _decrement_ram_value_at(self, idx: int):
        value = self._get_ram_value_at(idx)
        self._set_ram_value_at(idx, max(value - 1, 0))

    def _render_ram_cell(self, cell_idx, value):
        is_active = cell_idx == self.active_cell_idx
        is_candidate = cell_idx in self.candidate_cell_ids
        is_red = cell_idx in self.red_render

        x, y, w, h = self._get_ram_cell_rect(cell_idx)

        # Render cell background
        if is_active:
            color = (70, 70, 30)
        elif is_red:
            color = (150, 20, 20)
        elif is_candidate:
            color = (15, 45, 100)
        else:
            color = (20, 20, 20)
        pygame.draw.rect(self.window, color, [x, y, w, h])
        if cell_idx in self.no_render:
            return
        # Render cell ID label
        if is_active:
            color = (150, 150, 30)
        elif is_candidate:
            color = (20, 60, 200)
        else:
            color = (100, 150, 150)
        text = self.ram_cell_id_font.render(str(cell_idx), True, color, None)
        text_rect = text.get_rect()
        text_rect.topleft = (x + 2, y + 2)
        self.window.blit(text, text_rect)
        # Render cell value label
        if is_active:
            value = self.current_active_cell_input
        if value is not None:
            if is_active:
                color = (255, 255, 50)
            elif is_candidate:
                color = (30, 90, 255)
            else:
                color = (200, 200, 200)
            text = self.ram_cell_value_font.render(
                str(value), True, color, None)
            text_rect = text.get_rect()
            text_rect.bottomright = (x + w - 2, y + h - 2)
            self.window.blit(text, text_rect)

    def _get_ram_cell_rect(self, idx: int):
        row = idx // RAM_N_COLS
        col = idx % RAM_N_COLS
        x = round(self.ram_grid_anchor_left + col * 120 * (UPSCALE_FACTOR / 4))
        y = round(self.ram_grid_anchor_top + row * 50 * (UPSCALE_FACTOR / 4))
        w = RAM_CELL_WIDTH
        h = RAM_CELL_HEIGHT
        return x, y, w, h

    def _render_hover(self):
        cell_idx = self._get_cell_under_mouse()
        if cell_idx is not None and cell_idx != self.active_cell_idx:
            x, y, w, h = self._get_ram_cell_rect(cell_idx)
            hover_surface = pygame.Surface((w, h))
            hover_surface.set_alpha(60)
            hover_surface.set_colorkey((0, 0, 0))
            pygame.draw.rect(hover_surface, (255, 255, 255), [0, 0, w, h])
            self.window.blit(hover_surface, (x, y))

    def _get_cell_under_mouse(self):
        x, y = self.current_mouse_pos
        if x > self.ram_grid_anchor_left and y > self.ram_grid_anchor_top:
            col = int((x - self.ram_grid_anchor_left) //
                      (120 * (UPSCALE_FACTOR / 4)))
            row = int((y - self.ram_grid_anchor_top) //
                      (50 * (UPSCALE_FACTOR / 4)))
            if col < RAM_N_COLS and row < 16:
                return row * RAM_N_COLS + col
        return None

    def _unselect_active_cell(self):
        self.active_cell_idx = None
        self.current_active_cell_input = ""

    def find_causative_ram(self, x, y):
        """
        Goes over the entire RAM, manipulating it to observe possible changes
        in the current observation. Prints the RAM entry positions that are responsible
        for changes at pixel x, y.
        """
        ale = self.env.unwrapped.ale

        ram = ale.getRAM().copy()
        self.env.step(0)
        original_pixel = ale.getScreenRGB()[y, x]
        self._set_ram(ram)  # restore original RAM
        state = self.env._clone_state()

        self.candidate_cell_ids = []
        for i in tqdm(range(len(ram))):
            self.active_cell_idx = i
            # range(255):  # adding values != 0 causes Atari to crash
            for altered_value in [5]:
                self.current_active_cell_input = str(altered_value)
                self.env._restore_state(state)
                ale.setRAM(i, altered_value)
                self.env.step(0)
                new_frame = ale.getScreenRGB()
                self._render()
                new_pixel = new_frame[y, x]
                self._set_ram(ram)  # restore original RAM
                if np.any(new_pixel != original_pixel):
                    self.candidate_cell_ids.append(i)
                    break

        self.env._restore_state(state)
        self._unselect_active_cell()
        self._render()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description='OCAtari remgui.py Argument Setter')

    parser.add_argument('-g', '--game', type=str, default="Pong",
                        help='Game to be run')
    parser.add_argument('-hu', '--human', action='store_true',
                        help='Let user play the game.')
    parser.add_argument('-sf', '--switch_frame', type=int, default=0,
                        help='Swicht_modfis are applied to the game after this frame-threshold')
    parser.add_argument('-p', '--picture', type=int, default=0,
                        help='Takes a picture after the number of steps provided.')
    parser.add_argument('-a', '--agent', type=str, default='',
                        help="Path to the cleanrl trained agent to be loaded.")
    parser.add_argument('-nr', '--no_render', type=int, default=[],
                        help='Cells to not render.', nargs='+')
    parser.add_argument('-nra', '--no_render_all', action='store_true',
                        help='Not rendering any cell.')
    parser.add_argument('-m', '--mode', type=str, default='ram', choices=['ram', 'vision'],
                        help='Extraction mode.')
    parser.add_argument('-ls', '--load_state', type=str, default=None,
                        help='Path to the state to be loaded.')

    args = parser.parse_args()

    if args.no_render_all:
        args.no_render = list(range(128))

    renderer = Renderer(args.game, args.mode, args.no_render)

    if args.load_state:
        with open(args.load_state, "rb") as f:
            state, objects = pkl.load(f)
            renderer.env._ale.restoreState(state)
            renderer.env.objects = objects
            print(f"State loaded from {args.load_state}")

    def exit_handler():
        if renderer.no_render:
            print("\nno_render list: ")
            for i in sorted(renderer.no_render):
                print(i, end=" ")
            print("")
    atexit.register(exit_handler)

    renderer.run()
