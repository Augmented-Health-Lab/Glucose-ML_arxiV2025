import numpy as np
import pandas as pd
import copy
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

def rmse_summary(folder, type):
    """
    Generate summary statistics of RMSE values across different datasets.
    
    For each dataset's results file, calculates mean and standard deviation of
    RMSE values across different glucose ranges (overall, <70 mg/dL, 70-180 mg/dL, >180 mg/dL)
    and saves them to a summary CSV file.
    
    Args:
        folder (str): Path to folder containing RMSE result CSV files
        type (str): Type of summary working on
    
    Returns:
        None: Results are saved directly to the specified destination file
    """
    avg_rmse = []

    for file in os.listdir(folder):
        if file[-3:] == 'csv':
            df = pd.read_csv(os.path.join(folder, file))
            avg_rmse.append([file[:-9],
                            str(round(df['overall'].mean(), 2)) + ' (' + str(round(df['overall'].std(), 2)) +')',
                            str(round(df['< 70'].mean(), 2)) + ' (' + str(round(df['< 70'].std(), 2)) +')',
                            str(round(df['70 - 180'].mean(), 2)) + ' (' + str(round(df['70 - 180'].std(), 2)) +')',
                            str(round(df['> 180'].mean(), 2)) + ' (' + str(round(df['> 180'].std(), 2)) +')'])
        elif file == '1_OhioT1DM':
            df = pd.DataFrame([])
            for file2 in os.listdir(os.path.join(folder, file)):
                sub_df = pd.read_csv(os.path.join(folder, file, file2))
                df = pd.concat([df, sub_df])
            # print(df.shape)
            avg_rmse.append([file,
                            str(round(df['overall'].mean(), 2)) + ' (' + str(round(df['overall'].std(), 2)) +')',
                            str(round(df['< 70'].mean(), 2)) + ' (' + str(round(df['< 70'].std(), 2)) +')',
                            str(round(df['70 - 180'].mean(), 2)) + ' (' + str(round(df['70 - 180'].std(), 2)) +')',
                            str(round(df['> 180'].mean(), 2)) + ' (' + str(round(df['> 180'].std(), 2)) +')'])
    print(avg_rmse)

    df = pd.DataFrame(avg_rmse, columns=['dataset', 'Overall', '< 70', '70 - 180', '> 180'])
    df.to_csv(type + 'avg_rmse.csv', index=False)

# boxplot
def get_prediction_rmse(folder):
    """
    Extract RMSE values from result files and organize them by dataset.

    Reads RMSE data from result files, organizes them by dataset, and 
    sorts datasets by their numeric prefix for consistent visualization.

    Args:
        folder (str): Path to folder containing RMSE result CSV files

    Returns:
        tuple: (data, groups) where:
            - data is a list of lists containing RMSE values for each dataset
            - groups is a list of dataset names (labels) for visualization
    """
    df_list = {}
    for file in os.listdir(folder):
        if file[-3:] == 'csv':
            df = pd.read_csv(os.path.join(folder, file))
            df_list.update({file[:-9]: [int(i) for i in df['overall'].values if pd.notna(i)]})
            # break
        elif file == '1_OhioT1DM':
            df = pd.DataFrame([])
            for file2 in os.listdir(os.path.join(folder, file)):
                sub_df = pd.read_csv(os.path.join(folder, file, file2))
                df = pd.concat([df, sub_df])
            df_list.update({file: [int(i) for i in df['overall'].values if pd.notna(i)]})
            # break

    sorted_dict = dict(sorted(df_list.items(), key=lambda x: int(x[0].split('_')[0])))
    data = [sorted_dict[k] for k in sorted_dict.keys()]

    groups = [k.split('_')[1] for k in sorted_dict.keys()]
    groups[2] = 'BIG IDEAs'  # optional renaming
    groups[3] = 'DiaTrend'

    return data, groups

def get_boxplot(groups, zero_order_data, linear_reg_data):
    """
    Create a comparative boxplot visualization of model performances.
    
    Generates a side-by-side boxplot comparing zero-order hold and linear regression
    prediction models across different datasets, showing their RMSE distributions.
    
    Args:
        groups (list): List of dataset names (labels for x-axis)
        zero_order_data (list): List of lists containing RMSE values for zero-order hold model
        linear_reg_data (list): List of lists containing RMSE values for linear regression model
    
    Returns:
        None: The visualization is saved as a PNG file and displayed
    """
    # Create boxplot positions
    positions_zero = np.array(range(len(groups))) * 2.0
    positions_linear = positions_zero + 0.6
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.grid(True)

    # Boxplots
    bp1 = ax.boxplot(zero_order_data, positions=positions_zero, widths=0.5, patch_artist=True, medianprops=dict(color='black', linewidth=1))
    bp2 = ax.boxplot(linear_reg_data, positions=positions_linear, widths=0.5, patch_artist=True, medianprops=dict(color='black', linewidth=1))

    # Style boxplots
    for box in bp1['boxes']:
        box.set(facecolor='#4FF5D6')
    for box in bp2['boxes']:
        box.set(facecolor='#F48BBF')

    # X-axis setup
    mid_positions = (positions_zero + positions_linear) / 2
    ax.set_xticks(mid_positions)
    ax.set_xticklabels(groups, rotation=15, fontsize=11)  # Increased font size

    # Labels and legend with increased font size
    ax.set_ylabel('30-min BG Pred. RMSE (mg/dL)', fontsize=14)
    ax.legend([bp1["boxes"][0], bp2["boxes"][0]], 
              ['Zero-order Hold', 'Simple Linear Regression'], 
              fontsize=12, loc='upper left')
    ax.tick_params(axis='y', labelsize=11)  # Increase y-axis tick label size

    plt.tight_layout()
    plt.savefig('../Paper_Figures/Figure2_boxplot.png', bbox_inches='tight')
    plt.show()

def metrics_summary(folder, type):
    """
    Generate summary statistics of metrics values across different datasets.

    For each dataset's results file, calculates mean and standard deviation of metrics values 
    and saves them to a summary CSV file.
    
    Args:
        folder (str): Path to folder containing RMSE result CSV files
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
    Main function to orchestrate the summary and visualization process.
    
    This function:
    1. Computes RMSE summaries for both zero-order hold and linear regression results
    2. Extracts data for visualization
    3. Generates comparative boxplots
    
    The function uses hardcoded paths to the results folders and output destination.
    
    Returns:
        None: Results are saved as files and visualizations are displayed
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

        # rmse_summary(cur_folder, 'Evaluation_Results/zero_hold_')
        # rmse_summary(cur_folder, 'Evaluation_Results/linear_reg_')

    # generating boxplot
    # zero_order_data, groups = get_prediction_rmse(zero_hold_folder)
    # linear_reg_data, groups = get_prediction_rmse(linear_reg_folder)
    # get_boxplot(groups, zero_order_data, linear_reg_data)

if __name__ == "__main__":
    main()