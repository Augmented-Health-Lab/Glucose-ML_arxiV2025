# Data Filter: 70% Coverage

This section contains scripts designed to filter Continuous Glucose Monitoring (CGM) data based on daily coverage. The primary goal is to identify and save data from days with at least 70% coverage, ensuring high-quality data for further analysis.

## Overview of Scripts

- **`main.py`**: 
  - Contains the core functionality for filtering CGM data based on coverage.
  - Key functions:
    - `save_high_coverage_days`: Filters and optionally saves data from days with at least 70% coverage.
    - `process_folder`: Processes all CSV files in a folder, applying the `save_high_coverage_days` function.

## Key Parameter

- **Threshold-Based Filtering**: Filters data based on a user-defined threshold for maximum allowable gaps between consecutive readings (default is 15 minutes). Time gaps over this threshold will be taken as CGM missing period and were not taken as valid coverage time. 


## Running Instructions

1. **Ensure Dependencies**: Install the required Python packages using the following command:
   ```sh
   pip install pandas numpy
   ```
2. **Prepare Input Data**: Place the raw CGM data files (in CSV format) in a folder.

3. **Run the Script**: 
    To filter a single file:
    ```sh
    python3 main.py <file_path> <threshold> <save_path>
    ```

    ```sh
    python3 main.py "data/input.csv" 15 "data/high_coverage.csv"
    ```


## Notes
The input CSV files must contain a timestamp column as "timestamp" in datetime, and have the glucose value as "BGvalue" in dataframe.
Days with at least 70% coverage are saved to the specified output path.

## Output
Filtered data is saved as CSV files in the specified output folder or path.
A summary of daily coverage is printed to the console during execution.  