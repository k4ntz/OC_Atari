import pickle
import numpy as np
from pysr import PySRRegressor
from ocatari.utils import parser

def get_states_actions(buffer, simplify=True):
    all_states = np.array([st[0] for st in buffer] + [st[2] for st in buffer])
    to_remove = []
    if simplify:
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
        # verbosity=0
    )
    return model

def index(l, to_find):
    for i, el in enumerate(l):
        if el == to_find:
            return i
    return None

def perform_regression(x, y, vnames, tracked_ram):
    model = get_model()
    model.fit(x, y, variable_names=vnames)
    print("=== FINAL EQUATIONS ===")
    for eq in model.equations_["equation"]:
        print(f"ns[{tracked_ram}] = {eq}")

def get_regression_variables(states, next_states, state_poses, ram_pos, regressors):
    if regressors:
        vnames = [f"s{i}" for i in regressors] + [f"ss{i}" for i in regressors]
        reg_poses = [index(state_poses, r) for r in regressors]
        data = [states[:, r] for r in reg_poses]
        # extend data with the signed values of ram
        data.extend([states[:, r].astype(np.int8) for r in reg_poses])
        dataset = np.column_stack(data)
    else:
        vnames = [f"s{i}" for i in state_poses] + [f"ss{i}" for i in state_poses]
        # extend data with the signed values of ram
        dataset, state_poses = add_signed_states(states, state_poses)

    pos = index(state_poses, ram_pos)
    objective =  next_states[:, pos]

    return dataset, objective, vnames

def compute_accuracy(formulae, states, next_states):
    formulae = formulae.replace("=", "==") # replace assignment with comparison
    sns, ns = next_states.astype(np.int8).T, next_states.T
    ss, s  = states.astype(np.int8).T, states.T
    count_matches = np.sum(eval(formulae))
    print(f"Accuracy of regression: {count_matches / len(states) * 100}%")

def main():
    # args parsing
    parser.add_argument("-d", "--dataset", type=str, required=True,
                        help="dataset on which to perform the regression")
    parser.add_argument("-t", "--track", type=int, required=False,
                        help="ram position at state t+1 to predict from state t")
    parser.add_argument("-rr", "--reduce-ram", type=int, required=False, nargs="+",
                        help="the subset ram positions to use within regressors")
    parser.add_argument("-f", "--formulae", type=str, required=False, 
                        help="the formulae to test on the states (s), next_states (ns), or signed states (ss), and next signed states (nss)")
    opts = parser.parse_args()

    # loading dataset
    buffer = pickle.load(open(opts.dataset, "rb"))
    if opts.formulae:
        states, next_states, state_poses, _ = get_states_actions(buffer, simplify=False)
        compute_accuracy(opts.formulae, states, next_states)

    else:
        # performing regression
        states, next_states, state_poses, _ = get_states_actions(buffer, simplify=True)
        dataset, objective, vnames = get_regression_variables(states, next_states, state_poses, opts.track, opts.reduce_ram)
        perform_regression(dataset, objective, vnames, opts.track)

if __name__ == "__main__":
    main()