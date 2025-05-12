import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
from sklearn.linear_model import LinearRegression
pd.set_option('display.max_columns', None)

def split_into_continuous_series(df, past_sequence_length, future_offset, max_interval_minutes):
    """
    Split time series into continuous segments based on time gaps.

    Args:
        df: DataFrame containing glucose data
        past_sequence_length: Length of input sequence
        future_offset: Prediction horizon
        max_interval_minutes: Maximum gap (minutes) allowed within a continuous series

    Returns:
        List of DataFrames, each representing a continuous series
    """
    # Ensure DataFrame is sorted by timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
    df = df.sort_values('timestamp')

    # Calculate time differences
    time_diff = df['timestamp'].diff()

    # Find break points where interval > max_interval_minutes
    break_points = time_diff > pd.Timedelta(minutes=max_interval_minutes)

    # Create a series ID for each continuous sequence
    series_ids = break_points.cumsum()

    # Split the dataframe into list of series
    series_list = []
    for series_id in range(series_ids.max() + 1):
        series = df[series_ids == series_id].copy()
        # Only keep series with enough data points
        if len(series) > past_sequence_length + future_offset:
            series_list.append(series)

    return series_list

def get_seq_pred(series_list, past_sequence_length, future_offset):
  """
  Generate feature-target pairs from segmented time series for prediction.
  
  For each continuous series, this function creates sliding windows of:
  - Features: Sequence of 'past_sequence_length' consecutive readings
  - Target: Single reading at 'future_offset' steps ahead of the feature window
  
  Args:
      series_list (list): List of DataFrames representing continuous CGM series
      past_sequence_length (int): Number of past readings to use as features
      future_offset (int): How far ahead to predict (in number of readings)
      
  Returns:
      tuple: (features_list, trues_list) where:
          - features_list is a list of DataFrames, each containing past_sequence_length readings
          - trues_list is a list of Series objects, each containing a single future reading
  """
  features_list = []
  trues_list = []

  for series in series_list:
    for i in range(len(series) - past_sequence_length - future_offset):
      features_list.append(series.iloc[i:i + past_sequence_length])
      trues_list.append(series.iloc[i + past_sequence_length + future_offset-1])
    #   print(series.iloc[i:i + past_sequence_length])
    #   print(series.iloc[i + past_sequence_length + future_offset-1])
    # break
  return features_list, trues_list

from sklearn.metrics import mean_squared_error
# import numpy as np

def get_rmse(true, pred):
  """
  Calculate Root Mean Square Error between true and predicted values.
  
  Args:
      true (list or array): True values
      pred (list or array): Predicted values
      
  Returns:
      float: RMSE value, or None if calculation fails
  """
  # Calculate RMSE
  try:
    mse = mean_squared_error(true, pred)
    rmse = np.sqrt(mse)
    return rmse
  except:
    return None

def rmse_summary(trues, preds):
  """
  Calculate RMSE metrics across different clinically relevant glucose ranges.
  
  This function segments predictions into three clinically relevant glucose ranges:
  - Hypoglycemia: < 70 mg/dL
  - Normal range: 70-180 mg/dL
  - Hyperglycemia: > 180 mg/dL
  
  Args:
      trues (list or array): True glucose values
      preds (list or array): Predicted glucose values
      
  Returns:
      tuple: (overall_rmse, hypoglycemia_rmse, normal_range_rmse, hyperglycemia_rmse)
  """
  print('overall rmse:')
  rmse = get_rmse(trues, preds)
  print(rmse)

  print('< 70 rmse:')
  index_1 = [i for i, x in enumerate(trues) if x < 70]
  trues_1 = [trues[i] for i in index_1]
  preds_1 = [preds[i] for i in index_1]
  rmse_1 = get_rmse(trues_1, preds_1)
  print(rmse_1)

  print('70 - 180 rmse:')
  index_2 = [i for i, x in enumerate(trues) if 70 <= x <= 180]
  trues_2 = [trues[i] for i in index_2]
  preds_2 = [preds[i] for i in index_2]
  rmse_2 = get_rmse(trues_2, preds_2)
  print(rmse_2)

  print('> 180 rmse: ')
  index_3 = [i for i, x in enumerate(trues) if x > 180]
  trues_3 = [trues[i] for i in index_3]
  preds_3 = [preds[i] for i in index_3]
  rmse_3 = get_rmse(trues_3, preds_3)
  print(rmse_3)

  return rmse, rmse_1, rmse_2, rmse_3

def character_filter(df):
  """
  Filter out invalid character entries from the glucose data.
  
  This function removes:
  - NaN values
  - Empty strings
  - 'Low' and 'High' text values (non-numeric readings)
  
  Args:
      df (pd.DataFrame): DataFrame with CGM data
      
  Returns:
      pd.DataFrame: Filtered DataFrame with only valid numeric glucose values
  """
#   print('Character filter')
#   print(df.shape)
  df = df.dropna()
  df = df[df['BGvalue'].astype(str).str.strip() != ''] #remove empty strings
  df = df[df['BGvalue'].astype(str).str.strip() != 'Low'] #remove "Low" values
  df = df[df['BGvalue'].astype(str).str.strip() != 'High'] #remove "High" values
  df = df.reset_index(drop=True)
#   print(df.shape)
  return df

def timestamp_filter(df):
  """
  Filter time series data based on timestamp validity.
  
  This function removes readings that are too close in time, specifically:
  - Readings with time differences less than 0.5 minutes from the previous reading
  
  Args:
      df (pd.DataFrame): DataFrame with CGM data including 'timestamp' column
      
  Returns:
      pd.DataFrame: Filtered DataFrame with temporally valid readings
  """
#   print('Timestamp filter')
#   print(df.shape)
  df['timestamp'] = pd.to_datetime(df['timestamp'], infer_datetime_format=True)
  time_diffs = df['timestamp'].diff().dt.total_seconds() / 60  # Difference in minutes
  df.insert(len(df.columns), 'time_diffs', time_diffs)
  # rows_to_remove = df[(time_diffs >= 0) & (time_diffs <= .5)]
  # print(rows_to_remove)
  df = df[~df['time_diffs'].between(0, .5)] # remove BG values that time difference with last value < 0.5 min
  df = df.drop('time_diffs', axis=1)
#   print(df.shape)
  return df

def BGvalue_filter(df):
  """
  Filter physiologically implausible glucose rate-of-change values.
  
  This function removes readings where the rate of change in glucose values
  exceeds physiological plausibility (>20 mg/dL/minute), which likely
  represents sensor errors rather than true biological variation.
  
  Args:
      df (pd.DataFrame): DataFrame with CGM data including 'timestamp' and 'BGvalue' columns
      
  Returns:
      pd.DataFrame: Filtered DataFrame with physiologically plausible glucose changes
  """
#   print('BG filter')
#   print(df.shape)
  bg_diffs = df['BGvalue'].astype(int).diff()  # Absolute difference in BG values
  time_diffs = df['timestamp'].diff().dt.total_seconds() / 60
  df.insert(len(df.columns), 'bg_diffs', bg_diffs)
  bg_rate = bg_diffs / time_diffs
#   removed_rows = df[(abs(bg_rate) > 20) & (~bg_rate.isna())]
#   if not removed_rows.empty:
#     print(f"Removing {len(removed_rows)} rows with BG rate > 20 mg/dl/min:")
#     print(removed_rows[['timestamp', 'BGvalue', 'bg_diffs']])
    
  df = df[(abs(bg_rate) <= 20) | bg_rate.isna()]
  df = df.drop(['bg_diffs'], axis=1)
#   print(df.shape)
  return df
