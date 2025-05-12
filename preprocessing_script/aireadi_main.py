import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import json

def clean_aireadi_data(root, dst):
    """
    Processes AIR-EADI JSON data files and extracts blood glucose measurements.
    
    This function reads JSON files from the AIR-EADI dataset, extracts the continuous glucose 
    monitoring (CGM) data, normalizes it into a pandas DataFrame, selects relevant columns,
    and saves the processed data as CSV files.
    
    Args:
        root (str): Path to the root directory containing subject folders with JSON files
        dst (str): Path to destination directory where processed CSV files will be saved
    
    Returns:
        None: The function saves CSV files to the specified destination directory
    """
    os.makedirs(dst, exist_ok=True)
    for folder in os.listdir(root):
        file_name = [f for f in os.listdir(os.path.join(root, folder)) if f.endswith('.json')][0]
        file_path = os.path.join(root, folder, file_name)
        # print(file_name)
        with open(file_path, 'r') as f:
            data = json.load(f)

        cgm_data = data['body']['cgm']

        df = pd.json_normalize(
            cgm_data,
            sep='_',
            record_path=None,
            meta=None
        )

        df_selected = df[[
            'effective_time_frame_time_interval_start_date_time',
            'blood_glucose_value'
        ]]
        df_selected = df_selected.rename(columns={
            'effective_time_frame_time_interval_start_date_time': 'timestamp',
            'blood_glucose_value': 'BGvalue'
        })
        df_selected['timestamp'] = pd.to_datetime(df_selected['timestamp'], format='%Y-%m-%dT%H:%M:%SZ').dt.strftime('%Y-%m-%d %H:%M:%S')
        df_selected.to_csv(os.path.join(dst, file_name.split('.')[0] +'.csv'), index=False)
        
def main():
    """
    Main function that parses command-line arguments and initiates data processing.
    
    Expects two command-line arguments:
    1. Path to input folder containing AIR-EADI data
    2. Path to output folder where processed CSV files will be saved
    
    If incorrect number of arguments is provided, displays usage instructions and exits.
    
    Returns:
        None
    """
    if len(sys.argv) != 3:
        print("Usage: python aireadi_main.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    
    clean_aireadi_data(input_folder, output_folder)

if __name__ == "__main__":
    main()