#!/bin/bash

# This script preprocesses 5 public diabetes datasets downloaded by download_public_datasets.sh
# It assumes that the datasets are already downloaded into the "Original datasets" folder.

mkdir -p "../Preprocessed CGM/"
cd "../preprocessing_script/"

# ShanghaiT1DM dataset
chmod +x process_shanghait1dm.sh
./process_shanghait1dm.sh

# ShanghaiT2DM dataset
chmod +x process_shanghait2dm.sh
./process_shanghait2dm.sh

# big-idea-lab dataset
chmod +x process_big_idea_lab.sh
./process_big_idea_lab.sh

# cgmacros dataset
chmod +x process_cgmacros.sh
./process_cgmacros.sh

# UCHT1DM dataset
chmod +x process_uchtt1dm.sh
./process_uchtt1dm.sh