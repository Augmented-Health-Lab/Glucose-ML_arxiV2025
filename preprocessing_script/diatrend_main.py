import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

def clean_diatrend_data(root, dst):
    """
    Processes DiaTrend Excel data files and standardizes CGM data format.
    
    This function reads each Excel file from the specified root directory, 
    extracts data from the 'CGM' sheet, standardizes column names to match
    the project's conventions, and saves the processed data as CSV files.
    
    Args:
        root (str): Path to the directory containing DiaTrend Excel files
        dst (str): Path to destination directory where processed CSV files will be saved
    
    Returns:
        None: The function saves processed CSV files to the specified destination directory
    """
    # Ensure the output folder exists
    os.makedirs(dst, exist_ok=True)
    
    for file in os.listdir(root):
        df = pd.read_excel(os.path.join(root, file), sheet_name='CGM')
        df = df.rename(columns={'date': 'timestamp', 'mg/dl': 'BGvalue'})
        df.to_csv(os.path.join(dst, file.split('.')[0]) + '.csv', index=None)

def main():
    """
    Main function that parses command-line arguments and initiates data processing.
    
    Expects two command-line arguments:
    1. Path to input folder containing DiaTrend Excel files
    2. Path to output folder where processed CSV files will be saved
    
    If incorrect number of arguments is provided, displays usage instructions and exits.
    
    Returns:
        None
    """
    if len(sys.argv) != 3:
        print("Usage: python diatrend_main.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    
    clean_diatrend_data(input_folder, output_folder)


if __name__ == "__main__":
    main()