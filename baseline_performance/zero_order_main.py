from utils import *
import os
import sys
import numpy as np
import pandas as pd

def zero_order_hold(cgm_folder, dst, past_sequence_length, future_offset, max_interval_minutes):
  """
  Process CGM data files using a zero-order hold prediction method and calculate performance metrics.
  
  The zero-order hold method predicts future glucose values by assuming the future value
  will be equal to the most recent measurement (last value in the feature window).
  
  For each file in the specified folder, this function:
  1. Preprocesses the data (filtering invalid values and timestamps)
  2. Splits the data into continuous time series
  3. Creates feature-prediction pairs based on specified window parameters
  4. Applies zero-order hold (last value prediction) for future glucose values
  5. Calculates RMSE metrics for different glucose ranges
  6. Calculates MAE metrics for different glucose ranges

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
    preds = [i.BGvalue.values[-1] for i in features_list]
    trues = [int(i.BGvalue) for i in trues_list]
    
    # evaluate performance
    cur_res = []
    rmse, rmse_1, rmse_2, rmse_3 = rmse_summary(trues, preds)
    cur_res += [file.split('.')[0], rmse, rmse_1, rmse_2, rmse_3]
    mae, mae_1, mae_2, mae_3 = mae_summary(trues, preds)
    cur_res += [mae, mae_1, mae_2, mae_3]
    ceg_zones = CEG_summary(trues, preds)
    # print(ceg_zones)
    cur_res += list(ceg_zones.values())
    res.append(cur_res)
    # break

  df = pd.DataFrame(res, columns=['subject', 'overall (rmse)', '< 70 (rmse)', '70 - 180 (rmse)', '> 180 (rmse)',
                                  'overall (mae)', '< 70 (mae)', '70 - 180 (mae)', '> 180 (mae)'] + list(ceg_zones.keys()))
  df.to_csv(dst, index=False)


def main():
    """
    Main function to run zero-order hold prediction on CGM data
    
    Command line usage:
    python zero_order_main.py <cgm_folder> <destination> <past_sequence_length> <future_offset> <max_interval_minutes>
    
    Args:
        cgm_folder: Path to folder containing CGM data files
        dst: Path to save RMSE results
        past_sequence_length: Number of past measurements to use
        future_offset: Prediction horizon (in measurement intervals)
        max_interval_minutes: Maximum gap between readings to consider same series
        
    Returns:
        DataFrame with results
    """
    if len(sys.argv) != 6:
        print("Usage: python main.py <folder_path> <dstination> <past_sequence_length> <future_offset> <max_interval_minutes>")
        sys.exit(1)

    cgm_folder = sys.argv[1]
    dst = sys.argv[2]
    past_sequence_length = int(sys.argv[3])
    future_offset = int(sys.argv[4])
    max_interval_minutes = int(sys.argv[5])

    print(f"Running zero-order hold with parameters:")
    print(f"  CGM folder: {cgm_folder}")
    print(f"  Output: {dst}")
    print(f"  Past sequence length: {past_sequence_length}")
    print(f"  Future offset: {future_offset}")
    print(f"  Max interval minutes: {max_interval_minutes}")
    
    # Run the zero-order hold algorithm
    results = zero_order_hold(cgm_folder, dst, past_sequence_length, future_offset, max_interval_minutes)

    print(f"Results saved to {dst}")
    return results

if __name__ == "__main__":
    main()