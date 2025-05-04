#!/bin/bash

# Input and output paths
INPUT_FILE="../Glucose_measurements.csv"
OUTPUT_FOLDER="../8_T1DiabetesGranada"

# Run the Python script
python3 main.py "$INPUT_FILE" "$OUTPUT_FOLDER"