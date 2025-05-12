from utils import *
import os
import sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def single_linear_regression(features, future_time):
  """
  Predicts a future blood glucose value using simple linear regression.
  
  The function trains a linear model on the timestamps and glucose values 
  from the features dataframe, then predicts the glucose value at the specified 
  future timestamp.
  
  Args:
      features (pd.DataFrame): Dataframe containing 'timestamp' and 'BGvalue' columns
                              with historical blood glucose measurements
      future_time (datetime): Timestamp at which to predict the future glucose value
      
  Returns:
      float: Predicted blood glucose value at the specified future time
  """
  
  # Create and train the model
  timestamp = (features['timestamp'] - features['timestamp'].min()).dt.total_seconds()
  x = np.array(timestamp).reshape(-1, 1)

  pred_time = (future_time - features['timestamp'].min()).total_seconds()
  pred_time = np.array([pred_time]).reshape(-1, 1)
  # print(pred_time)

  # Create and train the model
  model = LinearRegression()
  model.fit(x, features.BGvalue.values)
  pred = model.predict(pred_time)
  return pred

def linear_regression(cgm_folder, dst, past_sequence_length, future_offset, max_interval_minutes):
  """
  Process CGM data files in a folder, apply linear regression for prediction,
  and calculate performance metrics.
  
  For each file in the specified folder, this function:
  1. Preprocesses the data (filtering invalid values)
  2. Splits the data into continuous time series
  3. Creates feature-prediction pairs based on specified window parameters
  4. Applies linear regression to predict future glucose values
  5. Calculates RMSE metrics for different glucose ranges
  
  Args:
      cgm_folder (str): Path to the folder containing CGM data files
      dst (str): Path where the results CSV will be saved
      past_sequence_length (int): Number of past measurements to use for prediction
      future_offset (int): How far into the future to predict (in measurement units)
      max_interval_minutes (int): Maximum gap allowed between readings to consider 
                                  them part of the same continuous series
      
  Returns:
      None: Results are saved directly to the specified destination file
  """
  res = []
  for file in os.listdir(cgm_folder):
    print('-----', file, '-----')
    df = pd.read_csv(os.path.join(cgm_folder, file))

    # if cgm_folder.split('Pre-processed CGM/')[1] in ['9_AI-READI/','7_ShanghaiT2DM/']:
    df = character_filter(df)
    df = timestamp_filter(df)
    df = BGvalue_filter(df)
    
    if df.empty:
      continue

    series_list = split_into_continuous_series(df, past_sequence_length, future_offset, max_interval_minutes)
    features_list, trues_list = get_seq_pred(series_list, past_sequence_length, future_offset)

    preds = []
    for i in range(len(features_list)):
      pred = single_linear_regression(features_list[i], trues_list[i].timestamp)
      preds.append(pred)

    trues = [int(i.BGvalue) for i in trues_list]
    rmse, rmse_1, rmse_2, rmse_3 = rmse_summary(trues, preds)
    res.append([file.split('.')[0], rmse, rmse_1, rmse_2, rmse_3])
    # break

  df = pd.DataFrame(res, columns=['subject', 'overall', '< 70', '70 - 180', '> 180'])
  df.to_csv(dst, index=False)

def main():
    """
    Main function to run linear regression prediction on CGM data
    
    Args:
        cgm_folder: Path to folder containing CGM data files
        dst: Path to save results
        past_sequence_length: Number of past measurements to use
        future_offset: Prediction horizon (in measurement intervals)
        max_interval_minutes: Maximum gap between readings to consider same series
        
    Returns:
        DataFrame with results
    """
    if len(sys.argv) != 6:
        print("Usage: python main.py <folder_path> <dstination> <past_sequence_length> <future_offset> <max_interval_minutes")
        sys.exit(1)

    cgm_folder = sys.argv[1]
    dst = sys.argv[2]
    past_sequence_length = int(sys.argv[3])
    future_offset = int(sys.argv[4])
    max_interval_minutes = int(sys.argv[5])
    
    print(f"Running linear regression hold with parameters:")
    print(f"  CGM folder: {cgm_folder}")
    print(f"  Output: {dst}")
    print(f"  Past sequence length: {past_sequence_length}")
    print(f"  Future offset: {future_offset}")
    print(f"  Max interval minutes: {max_interval_minutes}")
    
    # Run the zero-order hold algorithm
    results = linear_regression(cgm_folder, dst, past_sequence_length, future_offset, max_interval_minutes)
    
    print(f"Results saved to {dst}")
    return results

if __name__ == "__main__":
    main()