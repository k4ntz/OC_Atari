import pickle
import numpy as np
from pysr import PySRRegressor
from ocatari.utils import parser

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
        # print("deleted state", i)
        # if np.all(actions[:, i] == actions[0, i]):
        #     actions = np.delete(actions, i, axis=1)
        #     action_poses.remove(i)
    return states, next_states, state_poses, actions

def unsigned_to_signed(value, bits=8):
    max_signed = (1 << (bits - 1)) - 1
    if value <= max_signed:
        return value
    else:
        return value - (1 << bits)


def add_signed_states(states, state_poses):
    nstates, ncells = states.shape
    extended_states = np.zeros((nstates, 2 * ncells), dtype=int)
    extended_states[:, :ncells] = states
    for i, state in enumerate(states):
        signed_state = state.astype(np.int8)
        extended_states[i, ncells:] = signed_state
    state_poses.extend(state_poses)
    return extended_states, state_poses

def get_model():
    model = PySRRegressor(
        niterations = 50,  # < Increase me for better results
        maxsize = 10,
        binary_operators = ["+", "-"],
        elementwise_loss = "loss(prediction, target) = (prediction - target)^2",
    )
    return model

def index(l, to_find):
    for i, el in enumerate(l):
        if el == to_find:
            return i
    return None

def regress_ram_position(buffer, ram_pos):
    states, next_states, state_poses, _ = get_states_actions(buffer)
    vnames = [f"x{i}" for i  in state_poses] + [f"x{i}_s" for i  in state_poses] 
    states, state_poses = add_signed_states(states, state_poses)
    # print("Non constant ram indexes: ", state_poses)
    pos = index(state_poses, ram_pos)
    y =  next_states[:, pos]
    model = get_model()
    model.fit(states, y, variable_names=vnames)

def main():
    # args parsing
    parser.add_argument("-d", "--dataset", type=str, required=True,
                        help="dataset on which to perform the regression")
    parser.add_argument("-t", "--track", type=int, required=True,
                        help="ram position to regress")
    opts = parser.parse_args()

    # loading dataset
    buffer = pickle.load(open(opts.dataset, "rb"))
    # ram position to track
    to_track = opts.track
    # performing regression
    regress_ram_position(buffer, to_track)

if __name__ == "__main__":
    main()