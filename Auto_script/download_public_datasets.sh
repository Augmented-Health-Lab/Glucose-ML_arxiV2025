#!/bin/bash
# This script downloads 5 public diabetes datasets into Original datasets folder

mkdir -p "../Original datasets"

# ShanghaiT1DM and ShanghaiT2DM datasets
python3 ../preprocessing_script/download_shanghai_datasets.py
mkdir ../Original\ datasets/Shanghai_datasets
unzip ../Original\ datasets/diabetes_datasets.zip -d ../Original\ datasets/Shanghai_datasets
rm ../Original\ datasets/diabetes_datasets.zip
mv "../Original datasets/Shanghai_datasets/Shanghai_T1DM" "../Original datasets/"
mv "../Original datasets/Shanghai_datasets/Shanghai_T2DM" "../Original datasets/"
rm -rf "../Original datasets/Shanghai_datasets"

# big-idea-lab dataset https://physionet.org/content/big-ideas-glycemic-wearable/1.1.2/016/#files-panel
mkdir -p "../Original datasets/big_idea_lab"
# Loop to download files from 001 to 016 to only download the Dexcom files
for i in {1..16}; do
  num=$(printf "%03d" $i)
  echo "Downloading Dexcom_${num}.csv..."
  wget -P "../Original datasets/big_idea_lab" "https://physionet.org/files/big-ideas-glycemic-wearable/1.1.2/${num}/Dexcom_${num}.csv"
done

# cgmacros dataset https://physionet.org/content/cgmacros/1.0.0/
cd "../Original datasets/"
wget -r -N -c -np https://physionet.org/files/cgmacros/1.0.0/
mkdir -p "physionet.org/files/cgmacros/1.0.0/"
cd "physionet.org/files/cgmacros/1.0.0/"
# pwd
unzip CGMacros_dateshifted365.zip
mv "CGMacros/" '../../../../'
cd "../../../../"
# pwd
rm -rf "physionet.org"

# UCHT1DM dataset https://github.com/fisiologiacuantitativauc/UC_HT_T1DM
git clone https://github.com/fisiologiacuantitativauc/UC_HT_T1DM.git