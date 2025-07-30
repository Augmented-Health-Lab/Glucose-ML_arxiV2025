import numpy as np
import pandas as pd
import copy
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

def metrics_summary(folder, type):
    """
    Generate summary statistics of metrics values across different datasets.

    For each dataset's results file, calculates mean and standard deviation of metrics values 
    and saves them to a summary CSV file.
    
    Args:
        folder (str): Path to folder containing metrics result CSV files
        type (str): Type of summary working on
    
    Returns:
        None: Results are saved directly to the specified destination file
    """
    avg_metrics = []

    for file in os.listdir(folder):
        if file[-3:] == 'csv':
            df = pd.read_csv(os.path.join(folder, file))
            avg_metrics.append([file.split('_metrics.csv')[0],
                            str(round(df['overall (rmse)'].mean(), 2)) + ' (' + str(round(df['overall (rmse)'].std(), 2)) +')',
                            str(round(df['< 70 (rmse)'].mean(), 2)) + ' (' + str(round(df['< 70 (rmse)'].std(), 2)) +')',
                            str(round(df['70 - 180 (rmse)'].mean(), 2)) + ' (' + str(round(df['70 - 180 (rmse)'].std(), 2)) +')',
                            str(round(df['> 180 (rmse)'].mean(), 2)) + ' (' + str(round(df['> 180 (rmse)'].std(), 2)) +')', 
                            str(round(df['overall (mae)'].mean(), 2)) + ' (' + str(round(df['overall (mae)'].std(), 2)) +')',
                            str(round(df['< 70 (mae)'].mean(), 2)) + ' (' + str(round(df['< 70 (mae)'].std(), 2)) +')',
                            str(round(df['70 - 180 (mae)'].mean(), 2)) + ' (' + str(round(df['70 - 180 (mae)'].std(), 2)) +')',
                            str(round(df['> 180 (mae)'].mean(), 2)) + ' (' + str(round(df['> 180 (mae)'].std(), 2)) +')',
                            str(round(df['CEG_zoneA'].mean(), 2)) + ' (' + str(round(df['CEG_zoneA'].std(), 2)) +')',
                            str(round(df['CEG_zoneB'].mean(), 2)) + ' (' + str(round(df['CEG_zoneB'].std(), 2)) +')',
                            str(round(df['CEG_zoneC'].mean(), 2)) + ' (' + str(round(df['CEG_zoneC'].std(), 2)) +')',
                            str(round(df['CEG_zoneD'].mean(), 2)) + ' (' + str(round(df['CEG_zoneD'].std(), 2)) +')',
                            str(round(df['CEG_zoneE'].mean(), 2)) + ' (' + str(round(df['CEG_zoneE'].std(), 2)) +')'])
        elif file == '1_OhioT1DM':
            df = pd.DataFrame([])
            for file2 in os.listdir(os.path.join(folder, file)):
                sub_df = pd.read_csv(os.path.join(folder, file, file2))
                df = pd.concat([df, sub_df])
            # print(df.shape)
            avg_metrics.append([file,
                            str(round(df['overall (rmse)'].mean(), 2)) + ' (' + str(round(df['overall (rmse)'].std(), 2)) +')',
                            str(round(df['< 70 (rmse)'].mean(), 2)) + ' (' + str(round(df['< 70 (rmse)'].std(), 2)) +')',
                            str(round(df['70 - 180 (rmse)'].mean(), 2)) + ' (' + str(round(df['70 - 180 (rmse)'].std(), 2)) +')',
                            str(round(df['> 180 (rmse)'].mean(), 2)) + ' (' + str(round(df['> 180 (rmse)'].std(), 2)) +')',
                            str(round(df['overall (mae)'].mean(), 2)) + ' (' + str(round(df['overall (mae)'].std(), 2)) +')',
                            str(round(df['< 70 (mae)'].mean(), 2)) + ' (' + str(round(df['< 70 (mae)'].std(), 2)) +')',
                            str(round(df['70 - 180 (mae)'].mean(), 2)) + ' (' + str(round(df['70 - 180 (mae)'].std(), 2)) +')',
                            str(round(df['> 180 (mae)'].mean(), 2)) + ' (' + str(round(df['> 180 (mae)'].std(), 2)) +')',
                            str(round(df['CEG_zoneA'].mean(), 2)) + ' (' + str(round(df['CEG_zoneA'].std(), 2)) +')',
                            str(round(df['CEG_zoneB'].mean(), 2)) + ' (' + str(round(df['CEG_zoneB'].std(), 2)) +')',
                            str(round(df['CEG_zoneC'].mean(), 2)) + ' (' + str(round(df['CEG_zoneC'].std(), 2)) +')',
                            str(round(df['CEG_zoneD'].mean(), 2)) + ' (' + str(round(df['CEG_zoneD'].std(), 2)) +')',
                            str(round(df['CEG_zoneE'].mean(), 2)) + ' (' + str(round(df['CEG_zoneE'].std(), 2)) +')'])
    # print(avg_metrics)

    df = pd.DataFrame(avg_metrics, columns=['dataset', 'Overall (rmse)', '< 70 (rmse)', '70 - 180 (rmse)', '> 180 (rmse)',
                                            'Overall (mae)', '< 70 (mae)', '70 - 180 (mae)', '> 180 (mae)',
                                            'CEG_zoneA', 'CEG_zoneB', 'CEG_zoneC', 'CEG_zoneD', 'CEG_zoneE'])
    # print(df)
    df.to_csv(type + 'avg_metrics.csv', index=False)

def main():
    """
    Main function to orchestrate the summary process.
    
    This function:
    1. Computes all metrics summaries for both zero-order hold and linear regression results
    2. Extracts data for visualization
    3. Generates comparative boxplots
    
    The function uses hardcoded paths to the results folders and output destination.
    
    Returns:
        None: Results are saved as files. 
    """

    zero_hold_folder = 'zero_order_hold/'
    linear_reg_folder = 'linear_regression/'

    # saving rmse summary for zero-order hold and linear regression
    if not os.path.exists('Evaluation_Results'):
        os.makedirs('Evaluation_Results')
        
    for folder in [zero_hold_folder, linear_reg_folder]:
        # print(f'Processing folder: {folder}')
        os.makedirs(os.path.join('Evaluation_Results', folder), exist_ok=True)
        
        for subfolder in ['30mins', '45mins', '60mins']:
            cur_folder = os.path.join(folder, subfolder)
            if os.path.isdir(cur_folder):
                print(f'Processing subfolder: {cur_folder}')
                metrics_summary(cur_folder, os.path.join('Evaluation_Results', folder, subfolder + '_'))

if __name__ == "__main__":
    main()