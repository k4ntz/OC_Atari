import pickle
import numpy as np
from pysr import PySRRegressor
from ocatari.utils import parser
import re


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
        niterations = 100,  # < Increase me for better results
        maxsize = 10,
        binary_operators = ["+", "-", "*", "/", "max", "min", "mod", "cond", "greater", "logical_or", "logical_and"],
        unary_operators=["neg", "square", "exp", "log", "abs", "sqrt"],
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
    print("\n=== FINAL EQUATIONS ===")
    for eq in model.equations_["equation"]:
        formated_eq = re.sub(r's(\d+)', r's[\1]', eq)
        formated_eq = re.sub(r'a(\d+)', r'a[\1]', formated_eq)
        print(f"ns[{tracked_ram}] == {formated_eq}")

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

def compute_accuracy(formulae, states, next_states, actions):
    # formulae = formulae.replace("=", "==") # replace assignment with comparison
    formulae = formulae.replace("mod", "np.mod")
    formulae = formulae.replace("greater", "np.greater")
    formulae = formulae.replace("equal", "np.equal")
    formulae = formulae.replace("square", "np.square")
    formulae = formulae.replace("neg", "np.negative")
    formulae = formulae.replace("max", "np.maximum")
    sns, ns = next_states.astype(np.int8).T, next_states.T
    ss, s  = states.astype(np.int8).T, states.T
    a = actions.T
    count_matches = np.sum(eval(formulae))
    print(f"Accuracy of regression: {count_matches / len(states) * 100}%")


def add_actions(dataset, actions, vnames):
    #dataset shape: (n_samples, n_features)
    # actions shape: (n_samples, n_actions)
    # final shape: (n_samples, n_features + n_actions)
    n_samples, n_features = dataset.shape
    n_actions = actions.shape[1]
    dataset = np.column_stack((dataset, actions))
    vnames.extend([f"a{i}" for i in range(n_actions)])
    return dataset, vnames


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
    parser.add_argument("-ua", "--use-actions", action="store_true",
                        help="whether to use actions in the regression")
    opts = parser.parse_args()

    # loading dataset
    buffer = pickle.load(open(opts.dataset, "rb"))
    if opts.formulae:
        states, next_states, state_poses, actions = get_states_actions(buffer, simplify=False)
        compute_accuracy(opts.formulae, states, next_states, actions)

    else:
        # performing regression
        # states, next_states, state_poses, _ = get_states_actions(buffer, simplify=True)
        states, next_states, state_poses, actions = get_states_actions(buffer, simplify=True)
        dataset, objective, vnames = get_regression_variables(states, next_states, state_poses, opts.track, opts.reduce_ram)
        if opts.use_actions:
            dataset, vnames = add_actions(dataset, actions, vnames)
        perform_regression(dataset, objective, vnames, opts.track)

if __name__ == "__main__":
    main()