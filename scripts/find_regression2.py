import pickle
import numpy as np

buffer = pickle.load(open("transitions/Pong_data.pkl", "rb"))

state_poses = list(range(128))
action_poses = list(range(3))
states = np.array([st[0] for st in buffer]) 
actions = np.array([st[1] for st in buffer])
next_states = np.array([st[2] for st in buffer])
all_states = np.array([st[0] for st in buffer] + [st[2] for st in buffer])
for i in range(128):
    if np.all(all_states[:, i] == all_states[0, i]):
        state_poses.remove(i)
        states = np.delete(states, i, axis=1)
        states = np.delete(next_states, i, axis=1)
        print("deleted state", i)
    # if np.all(actions[:, i] == actions[0, i]):
    #     actions = np.delete(actions, i, axis=1)
    #     action_poses.remove(i)

