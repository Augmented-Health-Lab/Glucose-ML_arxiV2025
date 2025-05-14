#!/bin/bash

# Input and output folder paths
INPUT_FOLDER="../T1DEXI/LB_split"
OUTPUT_FOLDER="../2_T1DEXI"

# Run the Python script
python3 t1dexi_main.py "$INPUT_FOLDER" "$OUTPUT_FOLDER"