#!/bin/bash

python3 ../zero_order_main.py '../../Pre-processed CGM/2_T1DEXI/' '../zero_order_hold/30mins/2_T1DEXI_metrics.csv' 3 6 15
python3 ../zero_order_main.py '../../Pre-processed CGM/2_T1DEXI/' '../zero_order_hold/45mins/2_T1DEXI_metrics.csv' 7 9 15
python3 ../zero_order_main.py '../../Pre-processed CGM/2_T1DEXI/' '../zero_order_hold/60mins/2_T1DEXI_metrics.csv' 10 12 15