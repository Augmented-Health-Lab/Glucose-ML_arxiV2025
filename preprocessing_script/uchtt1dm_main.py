import os
import pandas as pd
import sys

def clean_uchtt1dm_data(base_folder, output_folder):
    """
    Cleans CGM data from the UCHTT1DM dataset by extracting data from Glucose.xlsx files
    in subfolders and saving the cleaned data into CSV files.

    Parameters:
    ----------
    base_folder : str
        Path to the base folder containing subfolders with Glucose.xlsx files.
    output_folder : str
        Path to the folder where cleaned CSV files will be saved.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all subfolders in the base folder
    for subfolder in os.listdir(base_folder):
        subfolder_path = os.path.join(base_folder, subfolder)

        # Check if it is a directory
        if os.path.isdir(subfolder_path):
            # Path to the Glucose.xlsx file
            excel_file = os.path.join(subfolder_path, 'Glucose.xlsx')

            # Check if the file exists
            if os.path.exists(excel_file):
                try:
                    # Read the Excel file
                    df = pd.read_excel(excel_file)

                    # Keep only the required columns
                    df = df[['Unnamed: 0', 'Value (mg/dl)']]

                    # Rename the columns
                    df = df.rename(columns={'Unnamed: 0': 'timestamp', 'Value (mg/dl)': 'BGvalue'})

                    # Remove rows with empty BGvalue
                    df = df.dropna(subset=['BGvalue'])

                    # Construct the output file path
                    output_file = os.path.join(output_folder, f"{subfolder}.csv")

                    # Save the DataFrame to a CSV file
                    df.to_csv(output_file, index=False)

                    print(f"Processed data from {excel_file} saved to {output_file}")
                except Exception as e:
                    print(f"Error processing file {excel_file}: {e}")

def main():
    """
    Main function to parse command-line arguments and execute the data cleaning process.
    """
    if len(sys.argv) != 3:
        print("Usage: python main.py <base_folder> <output_folder>")
        sys.exit(1)

    base_folder = sys.argv[1]
    output_folder = sys.argv[2]

    print(f"Cleaning data from {base_folder} and saving to {output_folder}")
    clean_uchtt1dm_data(base_folder, output_folder)

if __name__ == "__main__":
    main()