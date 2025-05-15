from scipy.stats import mannwhitneyu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from scipy.stats import mannwhitneyu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def Mann_whitney_test(rmse_df1, rmse_df2, df_label1, df_label2, results_file):
    """
    Perform Mann-Whitney U test on two datasets and save results to a file.
    
    Args:
        rmse_df1 (array-like): First dataset of RMSE values
        rmse_df2 (array-like): Second dataset of RMSE values
        df_label1 (str): Label for the first dataset
        df_label2 (str): Label for the second dataset
        results_file (str): Path to save the results
        
    Returns:
        None: Results are saved to the specified file
    """
    # Mann–Whitney U test
    U1, p_value = mannwhitneyu(rmse_df1, rmse_df2, alternative='two-sided')
    
    # Effect size: Rank-Biserial Correlation
    n1, n2 = len(rmse_df1), len(rmse_df2)
    U2 = n1*n2 - U1
    
    effect_size = 1 - (2 * U1) / (n1 * n2)
    N = n1 + n2
    z = (U1 - n1*n2/2 + 0.5) / np.sqrt(n1*n2 * (N + 1)/ 12)
    
    # Save results to file
    with open(results_file, 'a') as f:
        f.write(f"Comparison: {df_label1} vs {df_label2}\n")
        f.write(f"U statistic: {U1}\n")
        f.write(f"U statistic (alternative): {U2}\n")
        f.write(f"P-value: {p_value}\n")
        f.write(f"Effect size (rank-biserial correlation): {effect_size:.3f}\n")
        f.write(f"Z-score: {z:.3f}\n")
        f.write("-" * 50 + "\n")
    
    # Also print to console
    print(f"Comparison: {df_label1} vs {df_label2}")
    print(f"U statistic: {U1}")
    print(f"U statistic (alternative): {U2}")
    print(f"Z-score: {z:.3f}")
    print(f"P-value: {p_value}")
    print(f"Effect size (rank-biserial correlation): {effect_size:.3f}")
    print("-" * 50)

def main():
    """
    Main function to orchestrate the Mann-Whitney test between datasets.
    
    This function:
    1. Processes command-line arguments for two dataset RMSE files
    2. Sets up a results file for storing the statistical test results
    3. Loads and validates the input RMSE data
    4. Performs the Mann-Whitney U test and saves results
    
    The function requires four command-line arguments:
    - Path to first RMSE CSV file
    - Path to second RMSE CSV file 
    - Label for the first dataset
    - Label for the second dataset
    
    Results are saved to './mann_whitney_results.txt' and printed to console.
    
    Returns:
        None: Results are saved to file and displayed in console
    """
    # Check if correct number of arguments provided
    if len(sys.argv) < 5:
        print("Usage: python mann_whitney.py <file1> <file2> <label1> <label2>")
        print("Example: python mann_whitney.py ../zero_order_hold/4_BIG_IDEA_LAB_rmse.csv ../zero_order_hold/11_CGMacros_rmse.csv BIG_IDEA_LAB CGMacros")
        sys.exit(1)
    
    # Get command line arguments
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    label1 = sys.argv[3]
    label2 = sys.argv[4]
    
    # Define results file
    results_file = "./mann_whitney_results.txt"
    
    # Check if file exists, if not create it with header
    if not os.path.exists(results_file):
        with open(results_file, 'w') as f:
            f.write("Mann-Whitney U Test Results\n")
            f.write("=" * 50 + "\n\n")
    else:
        # Add a timestamp separator if appending to existing file
        with open(results_file, 'a') as f:
            f.write("\n\n" + "=" * 20 + f" New Test Run: {pd.Timestamp.now()} " + "=" * 20 + "\n\n")
    
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    rmse_df1 = df1['overall'].values
    rmse_df2 = df2['overall'].values

    Mann_whitney_test(rmse_df1, rmse_df2, label1, label2, results_file)

if __name__ == "__main__":
    main()