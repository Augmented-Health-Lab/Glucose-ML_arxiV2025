#!/bin/bash

# Input and output folder paths
BASE_FOLDER="../Original datasets/UC_HT_T1DM"
OUTPUT_FOLDER="../Pre-processed CGM/10_UCHTT1DM"

# Run the Python script
python3 uchtt1dm_main.py "$BASE_FOLDER" "$OUTPUT_FOLDER"