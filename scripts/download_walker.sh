#!/bin/bash

python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/walker2d_expert-v2.hdf5
python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/walker2d_random-v2.hdf5
python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/walker2d_medium-v2.hdf5
python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/walker2d_medium_replay-v2.hdf5
python scripts/generation/mujoco/stitch_dataset.py walker2d_expert-v2.hdf5 walker2d_medium-v2.hdf5 walker2d_medium_replay-v2.hdf5 walker2d_random-v2.hdf5 --output_file walker2d_random_medium_expert.hdf5 
python scripts/generation/mujoco/stitch_dataset.py walker2d_medium-v2.hdf5 walker2d_medium_replay-v2.hdf5 walker2d_random-v2.hdf5 --output_file walker2d_random_medium.hdf5
# i have checked
# python scripts/check_mujoco_datasets.py ./datasets/walker2d_random_medium_expert.hdf5 --env_name Walker2d-v3