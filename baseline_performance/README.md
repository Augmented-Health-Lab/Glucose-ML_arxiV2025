# 30-mins Glucose Prediction Baseline

This directory contains two baseline prediction models and evaluation for predicted CGM data across multiple diabetes datasets.

## Overview

The project includes implementations of:
1. **Zero-order Hold** - A naive prediction model that assumes future glucose values will be the same as the current value.
2. **Linear Regression** - A simple predictive model that extrapolates future glucose values based on historical trends.
3. **Evaluation** - Scripts for statistical comparison and visualization of model performance

## Directory Structure

```
baseline_performance/
├── zero_order_main.py         # Main script for zero-order hold predictions
├── linear_reg_main.py         # Main script for linear regression predictions
├── utils.py                   # Shared utility functions
├── figure2_script.py          # Script to generate summary boxplot
├── metrics_summary.py         # Script to generate summary mertics
├── Zero_order_script/         # Shell scripts for zero-order hold on different datasets
├── Linear_reg_script/         # Shell scripts for linear regression on different datasets
├── zero_order_hold/           # RMSE, MAE, CEG results from zero-order hold predictions
├── linear_regression/         # RMSE, MAE, CEG results from linear regression predictions
└── Evaluate_RMSE/             # Statistical evaluation scripts
```

## Prerequisites

- Python 3.7+
- Required packages:
  - pandas
  - numpy
  - scipy
  - matplotlib
  - scikit-learn

Install dependencies:

```bash
pip install pandas numpy scipy matplotlib scikit-learn
```

## Running Prediction Models

### Zero-order Hold

The zero-order hold model assumes the future glucose value will remain the same as the current value.

**Usage:**

```bash
python zero_order_main.py <cgm_folder> <destination> <past_sequence_length> <future_offset> <max_interval_minutes>
```

**Parameters:**
- `cgm_folder`: Path to folder containing CGM data files
- `destination`: Path for saving results CSV
- `past_sequence_length`: Number of historical points to consider (typically 1 for zero-order)
- `future_offset`: How far into the future to predict (in measurement intervals)
- `max_interval_minutes`: Maximum allowed gap between readings to consider as continuous series

**Example using provided scripts:**

```bash
cd Zero_order_script
chmod +x bil.sh
./bil.sh
```

### Linear Regression

The linear regression model predicts future glucose values based on a linear trend of historical values.

**Usage:**

```bash
python linear_reg_main.py <cgm_folder> <destination> <past_sequence_length> <future_offset> <max_interval_minutes>
```

**Parameters:** Same as zero-order hold

**Example using provided scripts:**

```bash
cd Linear_reg_script
chmod +x bil.sh
./bil.sh
```

## Statistical Evaluation

The Mann-Whitney test is used to compare RMSE distributions between pairs of datasets.

**Running Mann-Whitney Tests:**

```bash
cd Evaluate_RMSE
chmod +x mw_script.sh
./mw_script.sh
```

Results will be appended to `mann_whitney_results.txt`.

**Adding New Comparisons:**

Edit `mw_script.sh` to add new dataset comparisons:

```bash
python mann_whitney_main.py "<path_to_first_dataset_rmse.csv>" "<path_to_second_dataset_rmse.csv>" "<first_dataset_label>" "<second_dataset_label>"
```

## Generating Figures

The repository includes scripts for generating visualizations of model performance.

**Creating Box Plots:**

```bash
python figure2_script.py
```

This will generate boxplot comparisons of RMSE values across datasets.

## Generating Evaluation Summaries

The repository includes scripts for generating visualizations of model performance.

**Generating and Saving Metrics:**

```bash
python metrics_summary.py
```

This will generate all mertics (RMSE, MAE and Clarke Error Grid) across datasets with different prediction horizons (30mins, 45mins, and 60mins). 

## Dataset Format

Input CGM data files should contain at minimum:
- `timestamp`: Date and time of glucose readings
- `BGvalue`: Blood glucose values

RMSE results are stored in CSV files with columns:
- `subject`: Subject identifier
- `overall`: Overall RMSE
- `< 70`: RMSE for hypoglycemic range
- `70 - 180`: RMSE for normal range
- `> 180`: RMSE for hyperglycemic range

## Adding New Datasets

To add a new dataset:

1. Create a new shell script in the respective script folder (Zero_order_script or Linear_reg_script)
2. Follow the format of existing scripts, adjusting input and output paths
3. Run the script to generate RMSE, MAE, CEG results
4. Update the Mann-Whitney scripts if you want to run statistical comparisons