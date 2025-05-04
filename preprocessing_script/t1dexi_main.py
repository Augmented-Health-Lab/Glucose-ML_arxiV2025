import os
import pandas as pd
import sys

def clean_t1dexi_data(input_folder, output_folder):
    """
    Cleans CGM data from the T1DEXI dataset by selecting relevant columns and renaming them.

    Parameters:
    ----------
    input_folder : str
        Path to the folder containing the input CSV files.
    output_folder : str
        Path to the folder where cleaned CSV files will be saved.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get all file names in the input folder
    file_names = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    for input_file in file_names:
        input_file_path = os.path.join(input_folder, input_file)

        try:
            # Read the CSV file
            df = pd.read_csv(input_file_path)

            # Keep only the required columns and rename them
            df = df[['LBDTC', 'LBORRES']].rename(columns={'LBDTC': 'timestamp', 'LBORRES': 'BGvalue'})

            # Remove the last row (e.g., HBA1C row)
            df = df.iloc[:-1]

            # Extract the subject number from the input file name
            subject_number = os.path.basename(input_file).split('.')[0]

            # Construct the output file path
            output_file_path = os.path.join(output_folder, f"{subject_number}.csv")

            # Save the cleaned data to a new CSV file
            df.to_csv(output_file_path, index=False)

            print(f"Processed file saved to {output_file_path}")
        except Exception as e:
            print(f"Error processing file {input_file_path}: {e}")

def main():
    """
    Main function to parse command-line arguments and execute the data cleaning process.
    """
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    print(f"Cleaning data from {input_folder} and saving to {output_folder}")
    clean_t1dexi_data(input_folder, output_folder)

if __name__ == "__main__":
    main()