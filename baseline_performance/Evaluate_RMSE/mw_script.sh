#!/bin/bash

# BIG_IDEA_LAB vs CGMacros
python mann_whitney_main.py "../zero_order_hold/4_BIG_IDEA_LAB_rmse.csv" "../zero_order_hold/5_Diatrend_rmse.csv" "BIG_IDEA_LAB" "Diatrend"

python mann_whitney_main.py "../zero_order_hold/4_BIG_IDEA_LAB_rmse.csv" "../zero_order_hold/11_CGMacros_rmse.csv" "BIG_IDEA_LAB" "CGMacros"

python mann_whitney_main.py "../zero_order_hold/5_Diatrend_rmse.csv" "../zero_order_hold/6_ShanghaiT1DM_rmse.csv" "Diatrend" "ShanghaiT1DM"
