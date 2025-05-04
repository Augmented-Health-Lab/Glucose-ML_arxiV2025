import os
import xml.etree.ElementTree as ET
import csv
from datetime import datetime
import sys

def clean_ohiot1dm_data(input_folder, output_folder):
    """
    Cleans CGM data from the OhioT1DM dataset by parsing XML files and extracting glucose level events.

    Parameters:
    ----------
    input_folder : str
        Path to the folder containing the input XML files.
    output_folder : str
        Path to the folder where cleaned CSV files will be saved.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get all XML file names in the input folder
    file_names = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f)) and f.endswith('.xml')]

    for input_file in file_names:
        input_file_path = os.path.join(input_folder, input_file)

        try:
            # Parse the XML file
            tree = ET.parse(input_file_path)
            root = tree.getroot()

            # Get the patient ID
            patient_id = root.attrib['id']

            # Construct the output file path
            csv_filename = os.path.join(output_folder, f"{patient_id}.csv")

            # Open a CSV file for writing
            with open(csv_filename, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                # Write the header row
                writer.writerow(['timestamp', 'BGvalue'])

                # Find all <event> elements under <glucose_level>
                for event in root.find('glucose_level').findall('event'):
                    # Parse and reformat the timestamp
                    original_timestamp = event.attrib['ts']
                    formatted_timestamp = datetime.strptime(original_timestamp, "%d-%m-%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                    value = event.attrib['value']
                    # Write each event to the CSV file
                    writer.writerow([formatted_timestamp, value])

            print(f"Data has been written to {csv_filename}")
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
    clean_ohiot1dm_data(input_folder, output_folder)

if __name__ == "__main__":
    main()