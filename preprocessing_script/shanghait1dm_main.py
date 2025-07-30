import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

def determine_engine(filename):
    """
    Determine which Excel engine to use based on file extension
    """
    if filename.lower().endswith('.xlsx'):
        return 'openpyxl'
    elif filename.lower().endswith('.xls'):
        return 'xlrd'
    else:
        # Default to openpyxl for unknown extensions
        return 'openpyxl'

def clean_shanghait1dm_data(root, dst):
    """
    Processes Shanghai T1DM Excel data files and standardizes CGM data format.
    
    This function reads Excel files from the specified root directory, handles multiple
    files for the same subject by concatenating them, extracts relevant CGM data,
    standardizes column names, and saves the processed data as CSV files.
    
    The function identifies files belonging to the same subject by parsing the file name
    format where subject ID is the first part before an underscore.
    
    Args:
        root (str): Path to the directory containing Shanghai T1DM Excel files
        dst (str): Path to destination directory where processed CSV files will be saved
    
    Returns:
        None: The function saves processed CSV files to the specified destination directory
    """
    os.makedirs(dst, exist_ok=True)
    subj_dict = {}
    for file in os.listdir(root):
        if file.endswith('.xlsx') or file.endswith('.xls'):
            if file.split('_')[0] not in subj_dict:
                subj_dict.update({file.split('_')[0]: [file]})
            else:
                subj_dict[file.split('_')[0]].append(file)
    
    for subj in subj_dict.keys():
        if len(subj_dict[subj]) == 1:
            file_path = os.path.join(root, subj_dict[subj][0])
            engine = determine_engine(subj_dict[subj][0])
            try:
                df = pd.read_excel(file_path, sheet_name=subj_dict[subj][0].split('.')[0], engine=engine)
                df_selected = df[['Date', 'CGM (mg / dl)']].rename(columns={'Date': 'timestamp', 'CGM (mg / dl)': 'BGvalue'})
                df_selected.to_csv(os.path.join(dst, subj+'.csv'), index=None)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        else: # subject with multiple files
            subj_dict[subj].sort()
            df_list = []
            for file in subj_dict[subj]:
                file_path = os.path.join(root, file)
                engine = determine_engine(file)
                try:
                    df = pd.read_excel(file_path, sheet_name=file.split('.')[0], engine=engine)
                    df_list.append(df)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            
            if df_list:
                df = pd.concat(df_list, ignore_index=True)
                df_selected = df[['Date', 'CGM (mg / dl)']].rename(columns={'Date': 'timestamp', 'CGM (mg / dl)': 'BGvalue'})
                df_selected.to_csv(os.path.join(dst, subj+'.csv'), index=None)
            else:
                print(f"No data was successfully processed for subject {subj}")
    
def main():
    """
    Main function that parses command-line arguments and initiates data processing.
    
    Expects two command-line arguments:
    1. Path to input folder containing Shanghai T1DM Excel files
    2. Path to output folder where processed CSV files will be saved
    
    If incorrect number of arguments is provided, displays usage instructions and exits.
    
    Returns:
        None
    """
    if len(sys.argv) != 3:
        print("Usage: python shanghait1dm_main.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    
    clean_shanghait1dm_data(input_folder, output_folder)

if __name__ == "__main__":
    main()