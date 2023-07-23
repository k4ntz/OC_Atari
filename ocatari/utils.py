from argparse import ArgumentParser
from functools import partial
from gzip import GzipFile
from pathlib import Path
import keyboard
import numpy as np
import random
import sys
import select
# import tty
# import termios
import time
import atexit

try:
    import torch
    from torch import nn
    torch_imported = True
except ModuleNotFoundError:
    torch_imported = False


parser = ArgumentParser()
parser.add_argument("-p", "--path", type=str, help="path to the model", default=None)


test_parser = ArgumentParser()
test_parser.add_argument("-p", "--path", type=str, default=None,
                         help="path to the model")
test_parser.add_argument("-g", "--game", type=str, required=True,
                         help="game to evaluate (e.g. 'Pong')")
test_parser.add_argument("-i", "--iou", type=float, default=0.8,
                         help="Minimum iou for image saving (e.g. 0.7)")
test_parser.add_argument("-s", "--seed", type=float, default=None,
                         help="If provided, set the seed")


def make_deterministic(seed, mdp, states_dict=None):
    random.seed(seed)
    np.random.seed(seed)
    mdp.seed(seed)
    if torch_imported:
        torch.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    print(f"Set all environment deterministic to seed {seed}")

if torch_imported:
    class AtariNet(nn.Module):
        """ Estimator used by DQN-style algorithms for ATARI games.
            Works with DQN, M-DQN and C51.
        """
        def __init__(self, action_no, distributional=False):
            super().__init__()

            self.action_no = out_size = action_no
            self.distributional = distributional

            # configure the support if distributional
            if distributional:
                support = torch.linspace(-10, 10, 51)
                self.__support = nn.Parameter(support, requires_grad=False)
                out_size = action_no * len(self.__support)

            # get the feature extractor and fully connected layers
            self.__features = nn.Sequential(
                nn.Conv2d(4, 32, kernel_size=8, stride=4),
                nn.ReLU(inplace=True),
                nn.Conv2d(32, 64, kernel_size=4, stride=2),
                nn.ReLU(inplace=True),
                nn.Conv2d(64, 64, kernel_size=3, stride=1),
                nn.ReLU(inplace=True),
            )
            self.__head = nn.Sequential(
                nn.Linear(64 * 7 * 7, 512), nn.ReLU(inplace=True), nn.Linear(512, out_size),
            )

        def forward(self, x):
            assert x.dtype == torch.uint8, "The model expects states of type ByteTensor"
            x = x.float().div(255)

            x = self.__features(x)
            qs = self.__head(x.view(x.size(0), -1))

            if self.distributional:
                logits = qs.view(qs.shape[0], self.action_no, len(self.__support))
                qs_probs = torch.softmax(logits, dim=2)
                return torch.mul(qs_probs, self.__support.expand_as(qs_probs)).sum(2)
            return qs

        def draw_action(self, state):
            probs = self.forward(state)
            return probs.argmax()


def _load_checkpoint(fpath, device="cpu"):
    fpath = Path(fpath)
    with fpath.open("rb") as file:
        with GzipFile(fileobj=file) as inflated:
            return torch.load(inflated, map_location=device)


def _epsilon_greedy(obs, model, eps=0.001):
    if torch.rand((1,)).item() < eps:
        return torch.randint(model.action_no, (1,)).item(), None
    q_val, argmax_a = model(obs).max(1)
    return argmax_a.item(), q_val


# old_settings = termios.tcgetattr(sys.stdin)


# def restore_old_settings():
#     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


# atexit.register(restore_old_settings)


def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


class HumanAgent():
    def __init__(self):
        x = 0   # noqa
        # tty.setcbreak(sys.stdin.fileno())

    def draw_action(self, state):
        if isData():
            c = sys.stdin.read(1)
            if c == '\x1b':         # x1b is ESC
                exit(0)
            elif c == "a":
                return 2
            elif c == "e":
                return 1
        return 0


# def load_agent(opt, nb_actions=None):
#     if opt.path == "h":
#         return HumanAgent()
#     ckpt_path = Path(opt.path)


def load_agent(opt, nb_actions=None):
    ckpt_path = Path(opt.path)
    agent = AtariNet(nb_actions, distributional="c51" in opt.path)
    ckpt = _load_checkpoint(opt.path)
    agent.load_state_dict(ckpt["estimator_state"])
    return agent


class RandomAgent():
    """
    A agent acting randomly (following a uniform distribution).

    :param nb_actions
    """
    def __init__(self, nb_actions) -> None:
        self.nb_actions = nb_actions

    def draw_action(self, *args, **kwargs) -> int:
        return random.randint(0, self.nb_actions-1)