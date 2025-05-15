import pandas as pd


def character_filter(df):
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
#   print('Timestamp filter')
#   print(df.shape)
  df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
  time_diffs = df['timestamp'].diff().dt.total_seconds() / 60  # Difference in minutes
  df.insert(len(df.columns), 'time_diffs', time_diffs)
  # rows_to_remove = df[(time_diffs >= 0) & (time_diffs <= .5)]
  # print(rows_to_remove)
  df = df[~df['time_diffs'].between(0, .5)] # remove BG values that time difference with last value < 0.5 min
  df = df.drop('time_diffs', axis=1)
#   print(df.shape)
  return df

def BGvalue_filter(df):
#   print('BG filter')
#   print(df.shape)
  df['BGvalue'] = pd.to_numeric(df['BGvalue'], errors='coerce')
  bg_diffs = df['BGvalue'].diff()  # Absolute difference in BG values
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