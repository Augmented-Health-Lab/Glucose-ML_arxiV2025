import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import json

def clean_cgmacros_data(root, dst):
    """
    Processes CGM and macronutrient data files from a source directory.
    
    This function reads CSV files from each subject folder in the root directory,
    extracts the timestamp and relevant measurement data (based on output directory name),
    and saves a simplified CSV with standardized column names.
    
    Args:
        root (str): Path to the root directory containing subject folders with CSV files
        dst (str): Path to destination directory where processed CSV files will be saved
                  (The folder name is also used to determine which data column to extract)
    
    Returns:
        None: The function saves processed CSV files to the specified destination directory
    """
    os.makedirs(dst, exist_ok=True)
    type = dst.split('/')[2]
    print(type)
    
    for folder in os.listdir(root):
        folder_path = os.path.join(root, folder)
        # print(folder_path)
        if not os.path.isdir(folder_path) or folder.startswith('.'):
            print(f"Skipping {folder}: Not a directory or hidden file")
            continue
        try:
            file_name = [f for f in os.listdir(folder_path) if f.endswith('.csv')][0]
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            df_selected = df[['Timestamp', type]].rename(columns={'Timestamp': 'timestamp', type: 'BGvalue'})
            df_selected.to_csv(os.path.join(dst,  file_name.split('.')[0] + '.csv'), index=None)
            # break
        except:
            print(folder)

def main():
    """
    Main function that parses command-line arguments and initiates data processing.
    
    Expects two command-line arguments:
    1. Path to input folder containing subject folders with CGM/macronutrient data
    2. Path to output folder where processed CSV files will be saved
    
    If incorrect number of arguments is provided, displays usage instructions and exits.
    
    Returns:
        None
    """
    if len(sys.argv) != 3:
        print("Usage: python cgmacros_main.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    
    clean_cgmacros_data(input_folder, output_folder)
    
if __name__ == "__main__":
    main()