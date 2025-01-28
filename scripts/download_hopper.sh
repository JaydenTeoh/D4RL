#!/bin/bash

python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/hopper_expert-v2.hdf5
python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/hopper_random-v2.hdf5
python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/hopper_medium-v2.hdf5
python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/hopper_medium_replay-v2.hdf5
python scripts/generation/mujoco/stitch_dataset.py hopper_expert-v2.hdf5 hopper_medium-v2.hdf5 hopper_medium_replay-v2.hdf5 hopper_random-v2.hdf5 --output_file hopper_random_medium_expert.hdf5 
python scripts/generation/mujoco/stitch_dataset.py hopper_medium-v2.hdf5 hopper_medium_replay-v2.hdf5 hopper_random-v2.hdf5 --output_file hopper_random_medium.hdf5
# i have checked
# python scripts/check_mujoco_datasets.py ./datasets/hopper_random_medium_expert.hdf5 --env_name Hopper-v3