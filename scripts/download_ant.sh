#!/bin/bash

python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/ant_expert-v2.hdf5
python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/ant_random-v2.hdf5
python download.py http://rail.eecs.berkeley.edu/datasets/offline_rl/gym_mujoco_v2/ant_medium-v2.hdf5
python scripts/generation/mujoco/stitch_dataset.py ant_expert-v2.hdf5 ant_medium-v2.hdf5 ant_random-v2.hdf5 --output_file ant_random_medium_expert.hdf5 
python scripts/generation/mujoco/stitch_dataset.py ant_medium-v2.hdf5 ant_random-v2.hdf5 --output_file ant_random_medium.hdf5
# i have checked
# python scripts/check_mujoco_datasets.py ./datasets/ant_random_medium_expert.hdf5 --env_name Ant-v3