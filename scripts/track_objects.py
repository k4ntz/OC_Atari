import numpy as np
import pygame
from ocatari.core import OCAtari, UPSCALE_FACTOR
from tqdm import tqdm


from ocatari.core import OCAtari
import atexit

"""
This script can be used to display the n detected objects in the game.
Each object will be filled with a 20x20 pixels image, replacing the RAM display.
"""

OBJ_CELL_WIDTH = 100
OBJ_CELL_HEIGHT = 100

def _get_sides(obj):
    if obj.w > obj.h:
        xside = obj.w + 2
        if xside <= 10:
            xside, upscale = 10, 10
        elif xside <= 20:
            xside, upscale = 20, 5
        elif xside <= 33:
            xside, upscale = 33, 3
        else: 
            xside, upscale = 50, 2
        yside = obj.h + 2
    else:
        yside = obj.h + 2
        if yside <= 10:
            yside, upscale = 10, 10
        elif yside <= 20:
            yside, upscale = 20, 5
        elif yside <= 33:
            yside, upscale = 33, 3
        else: 
            yside, upscale = 50, 2
        xside = obj.w + 2
    return xside, yside, upscale


class Renderer:
    window: pygame.Surface
    clock: pygame.time.Clock
    env: OCAtari

    def __init__(self, env_name: str, hud: bool):
        self.env = OCAtari(env_name, mode="ram", hud=hud, render_mode="rgb_array",
                             render_oc_overlay=True, frameskip=1, obs_mode="obj")

        self.env.reset(seed=42)
        self.current_frame = self.env.render()
        self.max_objects = len(self.env._slots) # maximum number of objects to display
        self.obj_n_cols = self.max_objects // 7 + 1
        self._init_pygame(self.current_frame)
        self.paused = False

        self.current_keys_down = set()
        self.current_mouse_pos = None
        self.keys2actions = self.env.unwrapped.get_keys_to_action()

        self.obj_grid_anchor_left = self.env_render_shape[0] + 28
        self.obj_grid_anchor_top = 60
        self.track_color_change = False
        
        for i, obj in enumerate(self.env._slots):
            x, y, w, h = self._get_obj_cell_rect(i)
            obj_col = obj.rgb
            pygame.draw.rect(self.window, obj_col, [x-2, y-2, w+4, h+4], 2)

    def _init_pygame(self, sample_image):
        pygame.init()
        pygame.display.set_caption("OCAtari Environment")
        self.env_render_shape = sample_image.shape[:2]
        window_size = (self.env_render_shape[0] + self.obj_n_cols * 105 + 50, self.env_render_shape[1])
        self.window = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.obj_font = pygame.font.SysFont('Pixel12x10', 25)

    def run(self):
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                reward = self.env.step(action)[1]
                if reward != 0:
                    print(reward)
                    pass
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

                if event.key == pygame.K_r:  # 'R': reset
                    self.env.reset()

                elif [x for x in self.keys2actions.keys() if event.key in x]: #(event.key,) in self.keys2actions.keys() or [x for x in self.keys2actions.keys() if event.key in x]:  # env action
                    self.current_keys_down.add(event.key)

                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    pass

            elif event.type == pygame.KEYUP:  # keyboard key released
                if [x for x in self.keys2actions.keys() if event.key in x]:
                    self.current_keys_down.remove(event.key)

    def _render(self, frame=None):
        # self.window.fill((0, 0, 0))  # clear the entire window
        self._render_atari(frame)
        self._render_objects()
        pygame.display.flip()
        pygame.event.pump()

    def _render_atari(self, frame=None):
        if frame is None:
            frame = self.current_frame
        frame_surface = pygame.Surface(self.env_render_shape)
        pygame.pixelcopy.array_to_surface(frame_surface, frame)
        self.window.blit(frame_surface, (0, 0))
        self.clock.tick(60)

    def _render_objects(self):
        objects = self.env._objects
        num_objects = min(len(objects), self.max_objects)
        if len(objects) > self.max_objects:
            print(f"Warning: Too many objects detected ({len(objects)}). Displaying only the first {self.max_objects}.")
        for i in range(num_objects):
            self._render_object_cell(i, objects[i])

    def _render_object_cell(self, cell_idx, obj):
        x, y, w, h = self._get_obj_cell_rect(cell_idx)

        # Render object cell background
        color = (20, 20, 20)
        pygame.draw.rect(self.window, color, [x, y, w, h])

        # Render object details (you can customize this part)
        image_surface = pygame.Surface((w, h))
        img = self._get_obj_sprite(obj)
        pygame.surfarray.blit_array(image_surface, img)
        self.window.blit(image_surface, (x, y))

        if obj is not None:
            obj_init_color = self.window.get_at((x - 2, y - 2))
            border_color = obj.rgb
            if self.track_color_change and obj_init_color[:3] != border_color:
                pygame.draw.rect(self.window, (255, 20, 20), [x-2, y-2, w+4, h+4], 8)
                self.paused = True
                print(f"Object color changed for {obj}! Pausing the game. {obj_init_color} -> {border_color}")
            else:
                pygame.draw.rect(self.window, border_color, [x, y, w, h], 3)

    def _get_obj_sprite(self, obj):
        if obj is None:
            return np.ones((100, 100, 3), dtype=np.uint8) * 40
        xside, yside, upscale = _get_sides(obj)
        cx, cy = obj.center
        x = max(0, int(cx - xside / 2))
        y = max(0, int(cy - yside / 2))
        screen = self.env.getScreenRGB()
        sprite = screen[y:y+yside, x:x+xside,:].swapaxes(0,1).repeat(upscale, axis=0).repeat(upscale, axis=1)
        
        h, w, _ = sprite.shape
    
        # Create a new black (100x100) image (filled with zeros)
        padded_image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Calculate the position to center the original image on the 100x100 canvas
        top_left_y = (100 - h) // 2
        top_left_x = (100 - w) // 2
        
        # Place the smaller image in the center of the 100x100 black canvas
        padded_image[top_left_y:top_left_y + h, top_left_x:top_left_x + w, :] = sprite
        
        return padded_image

    def _get_obj_cell_rect(self, idx: int):
        row = idx // self.obj_n_cols
        col = idx % self.obj_n_cols
        x = self.obj_grid_anchor_left + col * (OBJ_CELL_WIDTH + 5)
        x = self.obj_grid_anchor_left + col * (OBJ_CELL_WIDTH + 5)
        y = self.obj_grid_anchor_top + row * (OBJ_CELL_HEIGHT + 5)
        y = self.obj_grid_anchor_top + row * (OBJ_CELL_HEIGHT + 5)
        w = OBJ_CELL_WIDTH
        h = OBJ_CELL_HEIGHT
        return x, y, w, h


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description='OCAtari remgui.py Argument Setter')

    parser.add_argument('-g', '--game', type=str, default="Seaquest",
                        help='Game to be run')
    parser.add_argument('-hud', '--hud', action='store_true',
                        help='Display HUD')


    args = parser.parse_args()

    renderer = Renderer(args.game, args.hud)

    renderer.run()
