# Preprocessing Scripts for CGM Datasets

This directory contains preprocessing scripts for cleaning and preparing Continuous Glucose Monitoring (CGM) datasets from the 10 sources listed in GlucoseML. Each script is tailored to handle the specific format and structure of the dataset it processes.

## Overview of Scripts
- **`ohiot1dm_main.py`**: Processes OhioT1DM dataset by parsing XML files and extracting glucose level events.
- **`t1dexi_main.py`**: Cleans T1DEXI dataset by selecting relevant columns, renaming them, and removing unnecessary rows.
- **`big_ideas_main.py`**: Cleans CGM data from the Big Idea Lab dataset by filtering rows with the 'EGV' event type and selecting relevant columns.
- **`diatrend_main.py`**: Cleans DiaTrend dataset by selecting relevant columns, renaming them, and saving into CSV files. 
- **`shanghait1dm_main.py`**: Cleans ShanghaiT1DM dataset by selecting relevant columns, renaming them, and saving into CSV files. 
- **`shanghait2dm_main.py`**: Cleans ShanghaiT2DM dataset by selecting relevant columns, renaming them, and saving into CSV files. 
- **`t1diabetesgranada_main.py`**: Processes T1DiabetesGranada dataset by extracting patient-specific data and saving it into CSV files.
- **`aireadi_main.py`**: Cleans AI-READI v2 dataset by selecting relevant columns, renaming them, and saving into CSV files. 
- **`uchtt1dm_main.py`**: Processes UCHTT1DM dataset by extracting data from `Glucose.xlsx` files in subfolders and saving the cleaned data into CSV files.
- **`cgmacros_main.py`**: Cleans CGMacros dataset by selecting relevant columns, renaming them, and saving into CSV files. 
- **`spit_csv.awk`**: Split the LB.csv file in T1DEXI dataset into subfiles for each individual.

## Running Instructions

Each script can be executed independently to process its corresponding dataset. Below are the general steps to run the scripts:

1. **Ensure Dependencies**: Install the required Python packages using the following command:
   ```sh
   pip install pandas
   ```
2. **Prepare Input Data**: Place the raw dataset files in the appropriate input folder as specified in the script.

3. **Run the Script**: Use the corresponding shell script to execute the preprocessing script. For example:

    To process the OhioT1DM dataset:
    ```sh
    bash process_ohiot1dm.sh
    ```

    To process the T1DEXI dataset:
    ```sh
    bash process_t1dexi.sh
    ```
4. **Output**: The cleaned data will be saved in the specified output folder.


## Notes
Ensure that the input and output folder paths are correctly specified in the shell scripts or command-line arguments.
Each script includes error handling to notify you of any issues during processing.
For further details, refer to the docstrings within each Python script. 

## Specifical instruction For T1DEXI dataset preprocessing:
When using `split_csv.awk` file to split the entire LB.csv file provided by T1DEXI dataset, using the following command in your terminal:
```sh
awk -f split_csv.awk LB.csv
```
And then, run the .sh file for T1DEXI preprocessing.

