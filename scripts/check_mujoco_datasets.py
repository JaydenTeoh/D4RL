"""
This script runs sanity checks all datasets in a directory.
Assumes all datasets in the directory are generated via mujoco and contain
the qpos/qvel keys.

Usage:

python check_mujoco_datasets.py <dirname>
"""
import numpy as np
import scipy as sp
import scipy.spatial
import h5py
import os
import argparse
import tqdm


def check_identical_values(dset, env_name):
    """ Check that values are not identical """
    check_keys = ['actions', 'observations', 'infos/qpos', 'infos/qvel']

    for k in check_keys:
        values = dset[k][:]

        values_0 = values[0]
        values_mid = values[values.shape[0]//2]
        values_last = values[-1]
        values = np.c_[values_0, values_mid, values_last].T
        dists = sp.spatial.distance.pdist(values)
        not_same = dists > 0
        assert np.all(not_same)


def check_qpos_qvel(dset, env_name):
    """ Check that qpos/qvel produces correct state"""
    import gym

    N = dset['rewards'].shape[0]
    qpos = dset['infos/qpos']
    qvel = dset['infos/qvel']
    obs = dset['observations']
    next_obs = dset['next_observations']
    terminals = dset['terminals']
    timeouts = dset['timeouts']

    env = gym.make(env_name)
    env.reset()
    print('checking qpos/qvel')
    for t in tqdm.tqdm(range(N)):
        env.set_state(qpos[t], qvel[t])
        env_obs = env.env.unwrapped._get_obs()
        obs_error = ((obs[t] - env_obs)**2).sum()
        assert obs_error < 1e-8
        if t > 0 and not terminals[t-1] and not timeouts[t-1]:
            next_obs_error = ((next_obs[t-1] - env_obs)**2).sum()
            assert next_obs_error < 1e-8

def check_num_samples(dset, env_name):
    """ Check that all keys have the same # samples """
    check_keys = ['actions', 'observations', 'rewards', 'timeouts', 'terminals', 'infos/qpos', 'infos/qvel']

    N = None
    for k in check_keys:
        values = dset[k]
        if N is None:
            N = values.shape[0]
        else:
            assert values.shape[0] == N


def check_reset_state(dset, env_name):
    """ Check that resets correspond approximately to the initial state """
    obs = dset['observations'][:]
    N = obs.shape[0]
    terminals = dset['terminals'][:]
    timeouts = dset['timeouts'][:]
    end_episode = (timeouts + terminals) > 0

    # Use the first observation as a reference initial state
    reset_state = obs[0]

    # Make sure all reset observations are close to the reference initial state

    # Take up to [:-1] in case last entry in dataset is terminal
    end_idxs = np.where(end_episode)[0][:-1]

    diffs = obs[1:] - reset_state
    dists = np.linalg.norm(diffs, axis=1)

    min_dist = np.min(dists)
    reset_dists = dists[end_idxs]  #don't add idx +1 because we took the obs[:1] slice
    print('max reset:', np.max(reset_dists))
    print('min reset:', np.min(reset_dists))

    assert np.all(reset_dists < (min_dist + 1e-2) * 5)


def print_avg_returns(dset, env_name):
    """ Print returns for manual sanity checking. """
    rew = dset['rewards'][:]
    terminals = dset['terminals'][:]
    timeouts = dset['timeouts'][:]
    end_episode = (timeouts + terminals) > 0

    all_returns = []
    returns = 0
    for i in range(rew.shape[0]):
        returns += float(rew[i])
        if end_episode[i]:
            all_returns.append(returns)
            returns = 0
    print('Avg returns:', np.mean(all_returns))
    print('# timeout:', np.sum(timeouts))
    print('# terminals:', np.sum(terminals))


CHECK_FNS = [print_avg_returns, check_qpos_qvel, check_reset_state, check_identical_values, check_num_samples]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str, help='Filename of HDF5 dataset')
    parser.add_argument('--env_name', type=str, help='Gym environment name')

    args = parser.parse_args()
    hfile = h5py.File(os.path.join(args.file_name), 'r')
    print('Checking:', args.file_name)
    for check_fn in CHECK_FNS:
        try:
            check_fn(hfile, args.env_name)
        except AssertionError as e:
            print('Failed test:', check_fn.__name__)
            raise e

