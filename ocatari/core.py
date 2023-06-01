import gymnasium as gym
import numpy as np
from ocatari.ram.extract_ram_info import detect_objects_raw, detect_objects_revised, init_objects, get_max_objects
from ocatari.vision.extract_vision_info import detect_objects_vision
from ocatari.vision.utils import mark_bb, to_rgba
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

AVAILABLE_GAMES = ["Assault", "Asterix", "Asteroids", "Atlantis", "BeamRider", "Berzerk", "Bowling", "Boxing",
                   "Breakout", "Carnival", "Centipede", "ChoppperCommand" "DemonAttack", "FishingDerby", "Freeway", "Frostbite", "Kangaroo",
                   "MontezumaRevenge", "MsPacman", "Pong", "Qbert", "Riverraid", "RoadRunner", "Seaquest", "Skiing", "SpaceInvaders",
                   "Tennis"]

class OCAtari:
    def __init__(self, env_name, mode="raw", hud=False, obs_mode="dqn", *args, **kwargs):
        """
        mode: raw/revised/vision/both
        """
        if "ALE/" in env_name: #case if v5 specified
            to_check = env_name[4:8]
            game_name = env_name.split("/")[1].split("-")[0].split("No")[0].split("Deterministic")[0]
        else:
            to_check = env_name[:4]
            game_name = env_name.split("-")[0].split("No")[0].split("Deterministic")[0]
        if to_check[:4] not in [gn[:4] for gn in AVAILABLE_GAMES]:
            print(colored("Game not available in OCAtari", "red"))
            print("Available games: ", AVAILABLE_GAMES)
            exit(1)
        self._env = gym.make(env_name, *args, **kwargs)
        self.game_name = game_name
        self.mode = mode
        self.hud = hud
        self.max_objects = []
        self._objects = init_objects(self.game_name, self.hud)
        if mode == "vision":
            self.detect_objects = detect_objects_vision
            self.step = self._step_vision
        elif mode == "raw":
            self.detect_objects = detect_objects_raw
            self.step = self._step_ram
        elif mode == "revised":
            self.max_objects = get_max_objects(self.game_name, self.hud)
            self.detect_objects = detect_objects_revised
            self.step = self._step_ram
        elif mode == "test":
            self.detect_objects_v = detect_objects_vision
            self.detect_objects_r = detect_objects_revised
            self.objects_v = init_objects(self.game_name, self.hud)
            self.step = self._step_test
        else:
            print(colored("Undefined mode for information extraction", "red"))
            exit(1)
        self._fill_buffer = lambda *args, **kwargs:None
        self._reset_buffer = lambda *args, **kwargs:None
        if obs_mode == "dqn":
            self._fill_buffer = self._fill_buffer_dqn
            self._reset_buffer = self._reset_buffer_dqn
        elif obs_mode == "ori":
            self._fill_buffer = self._fill_buffer_ori
            self._reset_buffer = self._reset_buffer_ori
        elif obs_mode is not None:
            print(colored("Undefined mode for observation (obs_mode), has to be one of ['dqn', 'ori', None]", "red"))
            exit(1)
        self.window = 4
        self._state_buffer = deque([], maxlen=self.window)
        self.action_space = self._env.action_space


    @property
    def _ale(self):
        return self._env.unwrapped.ale

    def _step_ram(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        if self.mode == "revised":
            self.detect_objects(self._objects, self._env.env.unwrapped.ale.getRAM(), self.game_name, self.hud)
        else:   # mode == "raw" because in raw mode we augment the info dictionary
            self.detect_objects(info, self._env.env.unwrapped.ale.getRAM(), self.game_name)
        self._fill_buffer()
        return obs, reward, truncated, terminated, info

    def _step_vision(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        self.detect_objects(self._objects, obs, self.game_name, self.hud)
        self._fill_buffer()
        return obs, reward, truncated, terminated, info

    def _step_test(self, *args, **kwargs):
        obs, reward, truncated, terminated, info = self._env.step(*args, **kwargs)
        self.detect_objects_r(self._objects, self._env.env.unwrapped.ale.getRAM(), self.game_name, self.hud)
        self.detect_objects_v(self.objects_v, obs, self.game_name, self.hud)
        self._fill_buffer()
        return obs, reward, truncated, terminated, info

    def _reset_buffer_dqn(self):
        for _ in range(self.window):
            self._state_buffer.append(
                torch.zeros(84, 84, device=DEVICE, dtype=torch.uint8)
            )
    
    def _reset_buffer_ori(self):
        for _ in range(self.window):
            self._state_buffer.append(
                torch.zeros(210, 160, 3, device=DEVICE, dtype=torch.uint8)
            )

    def reset(self, *args, **kwargs):
        self._reset_buffer()
        self._objects = init_objects(self.game_name, self.hud)
        return self._env.reset(*args, **kwargs)

    def _fill_buffer_dqn(self):
        state = cv2.resize(
            self._ale.getScreenGrayscale(), (84, 84), interpolation=cv2.INTER_AREA,
        )
        self._state_buffer.append(torch.tensor(state, dtype=torch.uint8,
                                               device=DEVICE))

    def _fill_buffer_ori(self):
        state = self._ale.getScreenRGB()
        self._state_buffer.append(torch.tensor(state, dtype=torch.uint8,
                                               device=DEVICE))

    def render(self, *args, **kwargs):
        return self._env.render(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self._env.close(*args, **kwargs)

    def seed(self, seed, *args, **kwargs):
        self._env.seed(seed, *args, **kwargs)

    @property
    def nb_actions(self):
        return self._env.unwrapped.action_space.n

    @property
    def dqn_obs(self):
        return torch.stack(list(self._state_buffer), 0).unsqueeze(0).byte()

    def set_ram(self, target_ram_position, new_value):
        """
        Directly manipulate a targeted RAM position
        """
        return self._env.unwrapped.ale.setRAM(target_ram_position, new_value)

    def get_ram(self):
        return self._ale.getRAM()

    def get_action_meanings(self):
        return self._env.env.env.get_action_meanings()

    def _get_obs(self):
        return self._env.env.env.unwrapped._get_obs()

    def _clone_state(self):
        return self._env.env.env.ale.cloneSystemState()

    def _restore_state(self, state):
        return self._env.env.env.ale.cloneSystemState()

    @property
    def objects(self):
        return [obj for obj in self._objects if obj]

    def render_explanations(self):
        coefs = [0.05, 0.1, 0.25, 0.6]
        rendered = torch.zeros_like(self._state_buffer[0]).float()
        for coef, state_i in zip(coefs, self._state_buffer):
            rendered += coef * state_i
        rendered = rendered.cpu().detach().to(int).numpy()
        for obj in self.objects:
            mark_bb(rendered, obj.xywh, color=obj.rgb)
        import matplotlib.pyplot as plt
        plt.imshow(rendered)
        rows, cells, colors = [], [], []
        columns = ["X, Y", "W, H", "R, G, B"]
        for obj in self.objects:
            rows.append(obj.category)
            cells.append([obj.xy, obj.wh, obj.rgb])
            colors.append(to_rgba(obj.rgb))
        # import ipdb; ipdb.set_trace()
        t_height = 0.03 * len(rows)
        table = plt.table(cellText=cells,
                          rowLabels=rows,
                          rowColours=colors,
                          colLabels=columns,
                          colWidths=[.2,.2,.3],
                          bbox=[0.1, 1.02, 0.8, t_height],
                          loc='top')
        table.set_fontsize(14)
        plt.subplots_adjust(top=0.8)
        plt.show()


class PositionHistoryGymWrapper(gym.Env):

    def __init__(self, ocatari_env : OCAtari) -> None:
        super().__init__()
        if ocatari_env.mode != "revised":
            print("ram only supported for env wrapper for now")
            exit()
        self.ocatari_env = ocatari_env
        self.reference_list = self._init_ref_vector()
        self.current_vector = np.zeros(4 * len(self.reference_list), dtype=np.float32)


    @property
    def observation_space(self):
        vl = len(self.reference_list) * 4
        return gym.spaces.Box(low=-2**63, high=2**63 - 2, shape=(vl, ), dtype=np.float32)


    @property
    def action_space(self):
        return self.ocatari_env.action_space


    def step(self, *args, **kwargs):
        _, reward, truncated, terminated, info = self.ocatari_env.step(*args, **kwargs)
        self._obj2vec()
        return self.current_vector, reward, truncated, terminated, info


    def reset(self, *args, **kwargs):
        _, info = self.ocatari_env.reset(*args, **kwargs)
        self._obj2vec()
        return self.current_vector, info


    def render(self, *args, **kwargs):
        return self.ocatari_env.render(*args, **kwargs)


    def close(self, *args, **kwargs):
        return self.ocatari_env.close(*args, **kwargs)


    def _init_ref_vector(self):
        reference_list = []
        obj_counter = {}
        for o in self.ocatari_env.max_objects:
            if o.category not in obj_counter.keys():
                obj_counter[o.category] = 0
            obj_counter[o.category] += 1
        for k in list(obj_counter.keys()):
            reference_list.extend([k for i in range(obj_counter[k])])
        return reference_list


    def _obj2vec(self):
        temp_ref_list = self.reference_list.copy()
        for o in self.ocatari_env.objects: # populate out_vector with object instance
            idx = temp_ref_list.index(o.category) #at position of first category occurance
            start = idx * 4
            flat = [item for sublist in o.h_coords for item in sublist]
            self.current_vector[start:start + 4] = flat #write the slice
            temp_ref_list[idx] = "" #remove reference from reference list
        for i, d in enumerate(temp_ref_list):
            if d != "": #fill not populated category instances wiht 0.0's
                self.current_vector[i*4:i*4+4] = [0.0, 0.0, 0.0, 0.0] #np.zeros(4, dtype=np.float32)