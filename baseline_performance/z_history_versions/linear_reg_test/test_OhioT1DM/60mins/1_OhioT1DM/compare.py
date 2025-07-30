import pandas as pd
import glob
import os

def calculate_averages_for_csv_files():
    """
    Read all CSV files in the current directory and calculate averages for each column in each file.
    Save results to a summary CSV file.
    """
    # Get all CSV files in the current directory
    csv_files = glob.glob("*.csv")
    
    print(f"Found {len(csv_files)} CSV files:")
    for file in csv_files:
        print(f"  - {file}")
    print("\n" + "="*80 + "\n")
    
    # Dictionary to store all results
    all_results = []
    
    # Process each CSV file
    for csv_file in sorted(csv_files):
        print(f"Processing: {csv_file}")
        print("-" * 60)
        
        try:
            # Read the CSV file
            df = pd.read_csv(csv_file)
            df = df.drop(columns=['subject'])
            print(f"Shape: {df.shape} (rows: {df.shape[0]}, columns: {df.shape[1]})")
            print(f"Columns: {list(df.columns)}")
            print()
            
            # Calculate averages for numeric columns only
            numeric_columns = df.select_dtypes(include=['number']).columns
            
            if len(numeric_columns) == 0:
                print("No numeric columns found in this file.")
            else:
                print("Column Averages:")
                averages = df[numeric_columns].mean()
                
                # Create a result dictionary for this file
                result_dict = {"filename": csv_file}
                
                for col, avg in averages.items():
                    print(f"  {col:<25}: {avg:.6f}")
                    result_dict[col] = avg
                
                all_results.append(result_dict)
            
            print("\n" + "="*80 + "\n")
            
        except Exception as e:
            print(f"Error processing {csv_file}: {str(e)}")
            print("\n" + "="*80 + "\n")
    
    # Save results to CSV file
    if all_results:
        results_df = pd.DataFrame(all_results)
        output_filename = "compare_summary.csv"
        results_df.to_csv(output_filename, index=False)
        print(f"Results saved to: {output_filename}")
        print(f"Summary shape: {results_df.shape}")
        print(f"Summary columns: {list(results_df.columns)}")
    else:
        print("No results to save.")

if __name__ == "__main__":
    calculate_averages_for_csv_files()