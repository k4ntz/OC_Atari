import pickle
import numpy as np
from pysr import PySRRegressor

BUFFER = pickle.load(open("transitions/Pong_data.pkl", "rb"))

def get_states_actions(buffer):
    all_states = np.array([st[0] for st in buffer] + [st[2] for st in buffer])
    to_remove = []
    for i in range(128):
        if np.all(all_states[:, i] == all_states[0, i]):
            to_remove.append(i)

    state_poses = list(range(128))
    # action_poses = list(range(3))
    states = np.array([st[0] for st in buffer]) 
    actions = np.array([st[1] for st in buffer])
    next_states = np.array([st[2] for st in buffer])
    for i in reversed(to_remove):
        state_poses.remove(i)
        states = np.delete(states, i, axis=1)
        next_states = np.delete(next_states, i, axis=1)
        print("deleted state", i)
        # if np.all(actions[:, i] == actions[0, i]):
        #     actions = np.delete(actions, i, axis=1)
        #     action_poses.remove(i)
    return states, next_states, state_poses, actions


def get_model(eq_file=None):
    model = PySRRegressor(
        niterations = 150,  # < Increase me for better results
        maxsize = 18,
        binary_operators = ["+", "-", "*", "/", "mod", "cond", "greater"],
        elementwise_loss = "loss(prediction, target) = (prediction - target)^2",
        # equation_file = f'pysr/{eq_file}'
    )
    return model

def index(l, to_find):
    for i, el in enumerate(l):
        if el == to_find:
            return i
    return None

def regress_ram_position(ram_pos):
    states, next_states, state_poses, _ = get_states_actions(BUFFER)
    print("Non constant ram indexes: ", state_poses)
    pos = index(state_poses, ram_pos)
    y =  next_states[:, pos]
    model = get_model(f"ram_{ram_pos}.csv")
    model.fit(states, y)
    equations = model.get_hof()
    print(equations)

regress_ram_position(49)