#!/bin/bash

python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/halfcheetah_expert-v2.hdf5
python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/halfcheetah_random-v2.hdf5
python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/halfcheetah_medium-v2.hdf5
python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/halfcheetah_medium_replay-v2.hdf5
python scripts/generation/mujoco/stitch_dataset.py halfcheetah_expert-v2.hdf5 halfcheetah_medium-v2.hdf5 halfcheetah_medium_replay-v2.hdf5 halfcheetah_random-v2.hdf5 --output_file halfcheetah_random_medium_expert.hdf5 
python scripts/generation/mujoco/stitch_dataset.py halfcheetah_medium-v2.hdf5 halfcheetah_medium_replay-v2.hdf5 halfcheetah_random-v2.hdf5 --output_file halfcheetah_random_medium.hdf5
# i have checked
# python scripts/check_mujoco_datasets.py ./datasets/halfcheetah_random_medium_expert.hdf5 --env_name HalfCheetah-v3