#!/bin/bash

# Input and output folder paths
INPUT_FOLDER="../Original datasets/big_idea_lab/"
OUTPUT_FOLDER="../Pre-processed CGM/4_BIG_IDEA_LAB/"

# Run the Python script
python3 big_ideas_main.py "$INPUT_FOLDER" "$OUTPUT_FOLDER"