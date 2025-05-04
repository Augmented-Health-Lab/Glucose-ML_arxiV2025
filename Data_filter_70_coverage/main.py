import pandas as pd
import numpy as np
import os
import sys

def save_high_coverage_days(file_path, threshold=15, save_path=None):
    """
    Counts the number of days with high and low CGM data coverage based on a specified threshold.
    Optionally saves data from high-coverage days.

    Parameters:
    ----------
    file_path : str
        The path to the CSV file containing CGM data. The file must have a 'timestamp' column in datetime format.
    threshold : int, optional
        The maximum allowable gap (in minutes) between consecutive readings to cap the time differences. 
        Default is 15 minutes.
    save_path : str, optional
        If provided, saves the filtered data from days with ≥70% coverage to this CSV path.
    """
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', format='mixed')
    df['date'] = df['timestamp'].dt.date

    coverage_list = []
    valid_dates = []

    for date, group in df.groupby('date'):
        group = group.sort_values('timestamp')
        time_diffs = group['timestamp'].diff().dt.total_seconds().div(60).dropna()
        capped_diffs = np.minimum(time_diffs, threshold)
        minutes_with_data = capped_diffs.sum()
        coverage_percent = minutes_with_data / 1440 * 100

        coverage_list.append({
            'date': date,
            'num_entries': len(group),
            'minutes_with_data': round(minutes_with_data),
            'coverage_percent': round(coverage_percent)
        })

        if coverage_percent >= 70:
            valid_dates.append(date)

    if save_path:
        filtered_df = df[df['date'].isin(valid_dates)].copy()
        filtered_df.to_csv(save_path, index=False)

def process_folder(folder_path, threshold, save_folder):
    """
    Processes all files in a folder, applying the save_high_coverage_days function.

    Parameters:
    ----------
    folder_path : str
        Path to the folder containing the input CSV files.
    threshold : int
        The maximum allowable gap (in minutes) between consecutive readings.
    save_folder : str
        Path to the folder where filtered CSV files will be saved.
    """
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for input_file in file_names:
        full_file_path = os.path.join(folder_path, input_file)
        save_path = os.path.join(save_folder, f"filtered_{input_file}")
        save_high_coverage_days(full_file_path, threshold, save_path)

def main():
    """
    Main function to parse command-line arguments and execute the process_folder function.
    """
    if len(sys.argv) != 4:
        print("Usage: python main.py <folder_path> <threshold> <save_folder>")
        sys.exit(1)

    folder_path = sys.argv[1]
    threshold = int(sys.argv[2])
    save_folder = sys.argv[3]

    print(f"Processing folder: {folder_path} with threshold: {threshold} and saving to: {save_folder}")
    process_folder(folder_path, threshold, save_folder)

if __name__ == "__main__":
    main()