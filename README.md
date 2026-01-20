# Glucose-ML: A collection of longitudinal diabetes datasets for development of robust AI solutions
Please cite the associated paper as follows:
- **Prioleau, T., Lu, B. and Cui, Y., 2025. Glucose-ML: A collection of longitudinal diabetes datasets for development of robust AI solutions. arXiv preprint arXiv:2507.14077.
https://doi.org/10.48550/arXiv.2507.14077**

## Abstract
Artificial intelligence (AI) algorithms are a critical part of state-of-the-art digital health technology for diabetes management. Yet, access to large high-quality datasets creates barriers that impede development of robust AI solutions. To accelerate development of transparent, reproducible, and robust AI solutions, we present Glucose-ML, a collection of 10 publicly available diabetes datasets, released within the last 7 years (i.e. 2018 - 2025). The Glucose-ML collection comprises over 300,000 days of continuous glucose monitor (CGM) data with a total of 38 million glucose samples, and was collected from 2500+ people, across 4 countries, living with type 1 diabetes, type 2 diabetes, prediabetes, and no diabetes. To support researchers and innovators with using this rich collection of diabetes datasets, we present a comparative analysis to guide algorithm developers with data selection, and to elicit strengths and weaknesses of each dataset. In addition, we conduct a case study focused on a common AI task within the field (i.e., blood glucose prediction). Through this study, we provide a benchmark for short-term blood glucose prediction across all 10 publicly available diabetes datasets within the Glucose-ML collection. We also show that the same algorithm can have significantly different prediction results when developed/evaluated with different datasets. Findings from this study are used to inform recommendations for developing robust AI solutions within the diabetes or broader health domain.

---
## About

This repository contains the code developed for analysis of 10 publicly available diabetes datasets curated in the Glucose-ML collection published here: https://doi.org/10.48550/arXiv.2507.14077. This repository does _not_ host any of the datasets directly but _only_ associated code for working with each dataset. Table 1 in the above referenced paper includes direct links for accessing and downloading the open-access datasets (5 out of 10) and direct links for requesting access to the controlled-access datasets (5 out of 10) in the Glucose-ML collection. 

To support easy of use, this repository also provides automated scripts in the ```Auto_script/``` directory for downloading, preprocessinig (or harmonizing), and jointly analyzing the open-access diabetes datasets (5) in the Glucose-ML collection, including baseline evaluation of two naive baseline methods for the common ML task of blood glucose prediction.  

## Requirements

To set up the environment and install the required dependencies, follow these steps:

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Mac/Linux
   # For Windows:
   # venv\Scripts\activate
   ```
Then, install the required packages:
```sh
pip install -r requirements.txt
```

## Structure

1. ```preprocessing_script/```
    Contains scripts for cleaning and preparing raw datasets for the task of blood glucose prediction. 

2. ```Data_filter_70_coverage/```
    Includes scripts for filtering CGM data to retain days with at least 70% CGM data coverage. 
3. ```baseline_performance/```
    Contains scripts and results for implementing two naive blood glucose prediction models. 
4. ```Paper_Figures/```
    Includes comparative analysis figures presented in the paper.

5. ```Script_for_Figures/```
    Includes the Jupyter notebook files used to plot the figures presented in the paper.

6. ```Script_for_Tables/```
    Includes the Jupyter notebook files to calculate the data for the tables included in the paper.

7. ```Auto_script/```
    Contains automation scripts for streamlining the workflow. Includes:
    - ```download_public_datasets.sh```: Automatically downloads the 5 public diabetes datasets into the "Original datasets" folder
    - ```preprocess.sh```: Processes the downloaded datasets into standardized formats for analysis
    - ```zero_order_auto_script.sh```: Automates the execution of all zero-order prediction model scripts
    - ```linear_reg_auto_script.sh```: Automates the execution of all linear regression model scripts

## Preprocessing

To preprocess the datasets, navigate to the ```preprocessing_script/``` folder and follow the instructions in its [README](./preprocessing_script/README.md).

## Case Study: Blood glucose prediction

For baseline performance and blood glucose prediction case studies, refer to the ```baseline_performance/``` folder and its [README](./baseline_performance/README.md).

## Comparative Analysis

 ```Paper_Figures/``` includes the figures presented in the paper. For the code to plot those figures and the tables included in the paper, please refer to the ```Script_for_Figures/``` and ```Script_for_Tables/```.

## Automation Scripts
This project includes several automation scripts to streamline the workflow from data acquisition to model evaluation. The scripts are located in the ```Auto_script/``` folder and can be executed in sequence to reproduce the full pipeline.

```bash
cd Auto_script
chmod +x *.sh   # Make all scripts executable
./download_public_datasets.sh   # Download Public Datasets
./preprocess.sh   # Preprocess the Datasets
./zero_order_auto_script.sh   # Run Zero-Order Prediction Models
./linear_reg_auto_script.sh   #Run Linear Regression Prediction Models
```

After running these scripts, all 5 public CGM datasets will be downloaded, preprocessed, and analyzed with both baseline prediction models. Results will be available in the ```baseline_performance/``` folder and its [README](./baseline_performance/README.md) described in detail.

## Questions, Comments or Feedback

Please reach out to the Principal Investigator: Temiloluwa Prioleau, PhD ([tpriole@emory.edu](mailto:tpriole@emory.edu)).

## Project Contributors
- Baiying Lu
- Yanjun Cui

## License

This project is licensed under the MIT License.
