import os
import pandas as pd
import sys

def clean_t1diabetesgranada_data(input_file, output_folder):
    """
    Cleans CGM data from the T1DiabetesGranada dataset by grouping by Patient_ID,
    creating a timestamp column, and saving the cleaned data into separate CSV files.

    Parameters:
    ----------
    input_file : str
        Path to the input CSV file containing the raw data.
    output_folder : str
        Path to the folder where cleaned CSV files will be saved.
    """
    # Read the input CSV file
    df = pd.read_csv(input_file)

    # Process each Patient_ID
    for patient_id, patient_data in df.groupby('Patient_ID'):
        try:
            # Create the "timestamp" column by combining "Measurement_date" and "Measurement_time"
            patient_data['timestamp'] = patient_data['Measurement_date'] + ' ' + patient_data['Measurement_time']

            # Rename the "Measurement" column to "BGvalue"
            patient_data = patient_data.rename(columns={'Measurement': 'BGvalue'})

            # Keep only the required columns
            patient_data = patient_data[['timestamp', 'BGvalue']]

            # Ensure the output folder exists
            os.makedirs(output_folder, exist_ok=True)

            # Construct the output file path
            output_file = os.path.join(output_folder, f"{patient_id}.csv")

            # Save the processed data to a new CSV file
            patient_data.to_csv(output_file, index=False)

            print(f"Processed data for Patient_ID {patient_id} saved to {output_file}")
        except Exception as e:
            print(f"Error processing data for Patient_ID {patient_id}: {e}")

def main():
    """
    Main function to parse command-line arguments and execute the data cleaning process.
    """
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_file> <output_folder>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_folder = sys.argv[2]

    print(f"Cleaning data from {input_file} and saving to {output_folder}")
    clean_t1diabetesgranada_data(input_file, output_folder)

if __name__ == "__main__":
    main()