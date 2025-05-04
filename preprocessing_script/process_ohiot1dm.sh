#!/bin/bash

# Process OhioT1DM 2018 dataset
python3 ohiot1dm_main.py "../OhioT1DM 2020/2018/train" "../1_OhioT1DM/2018/train"
python3 ohiot1dm_main.py "../OhioT1DM 2020/2018/test" "../1_OhioT1DM/2018/test"

# Process OhioT1DM 2020 dataset
python3 ohiot1dm_main.py "../OhioT1DM 2020/2020/train" "../1_OhioT1DM/2020/train"
python3 ohiot1dm_main.py "../OhioT1DM 2020/2020/test" "../1_OhioT1DM/2020/test"