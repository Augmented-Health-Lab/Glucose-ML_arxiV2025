import pandas as pd
import os
import sys

def clean_big_idea_lab_data(input_folder, output_folder):
    """
    Cleans CGM data from the Big Idea Lab dataset by filtering rows with 'EGV' event type
    and selecting relevant columns.

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

            # Filter rows where Event Type is "EGV"
            filtered_df = df[df['Event Type'] == 'EGV']

            # Select and rename the required columns
            processed_df = filtered_df[['Timestamp (YYYY-MM-DDThh:mm:ss)', 'Glucose Value (mg/dL)']].rename(
                columns={'Timestamp (YYYY-MM-DDThh:mm:ss)': 'timestamp', 'Glucose Value (mg/dL)': 'BGvalue'}
            )

            # Construct the output file path
            output_file_path = os.path.join(output_folder, input_file)

            # Save the processed DataFrame to a CSV file
            processed_df.to_csv(output_file_path, index=False)

            print(f"Processed data saved to {output_file_path}")
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
    clean_big_idea_lab_data(input_folder, output_folder)

if __name__ == "__main__":
    main()