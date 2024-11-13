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

def perform_regression(x, y, vnames):
    model = get_model()
    model.fit(x, y, variable_names=vnames)

def get_regression_variables(states, next_states, state_poses, ram_pos, regressors):
    if regressors:
        vnames = [f"x{i}" for i in regressors] + [f"x{i}_s" for i in regressors]
        reg_poses = [index(state_poses, r) for r in regressors]
        data = [states[:, r] for r in reg_poses]
        # extend data with the signed values of ram
        data.extend([states[:, r].astype(np.int8) for r in reg_poses])
        dataset = np.column_stack(data)
    else:
        vnames = [f"x{i}" for i in state_poses] + [f"x{i}_s" for i in state_poses]
        # extend data with the signed values of ram
        dataset, state_poses = add_signed_states(states, state_poses)

    pos = index(state_poses, ram_pos)
    objective =  next_states[:, pos]

    return dataset, objective, vnames

def compute_accuracy(wp, state_poses, states, next_states, ram_pos):
    weights, positions = [], []
    shift = len(state_poses) // 2
    for i, el in enumerate(wp):
        if i%2 == 0:
            weights.append(int(el))
        else:
            if el[-1] == 's':
                pos = int(el[:-1])
                pos = index(state_poses, pos)
                positions.append(shift + pos)
            else:
                pos = int(el)
                pos = index(state_poses, pos)
                positions.append(pos)

    nstates, _ = states.shape
    computed_states = np.zeros(nstates)
    for pos, w in zip(positions, weights):
        computed_states += w * states[:, pos]
    count_matches = np.sum(computed_states == next_states[:, ram_pos])
    print(f"Accuracy of regression: {count_matches / nstates * 100}%")

def main():
    # args parsing
    parser.add_argument("-d", "--dataset", type=str, required=True,
                        help="dataset on which to perform the regression")
    parser.add_argument("-t", "--track", type=int, required=True,
                        help="ram position to regress")
    parser.add_argument("-fr", "--force-regressors", type=int, required=False, nargs="+",
                        help="ram positions to use as regressors")
    parser.add_argument("-ca", "--compute-accuracy", type=str, required=False, nargs="+",
                        help="weights and positions to linearly combine to compute the ram position. Enter a sequence of weight and position")
    opts = parser.parse_args()

    # loading dataset
    buffer = pickle.load(open(opts.dataset, "rb"))
    states, next_states, state_poses, _ = get_states_actions(buffer)
    # print("Non constant ram indexes: ", state_poses)
    # ram position to track
    to_track = opts.track
    dataset, objective, vnames = get_regression_variables(states, next_states, state_poses, to_track, opts.force_regressors)

    if opts.compute_accuracy:
        compute_accuracy(opts.compute_accuracy, state_poses, dataset, next_states, index(state_poses, to_track))
    else:
        # performing regression
        perform_regression(dataset, objective, vnames)

if __name__ == "__main__":
    main()