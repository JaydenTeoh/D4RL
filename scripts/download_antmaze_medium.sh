#!/bin/bash

python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/ant_maze_new/Ant_maze_big-maze_noisy_multistart_True_multigoal_True_sparse.hdf5 antmaze_medium_dense.hdf5
python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/ant_maze_new/Ant_maze_medium_eval_noisy_multistart_True_multigoal_True_sparse.hdf5 antmaze_medium_dense_eval.hdf5