# Glucose-ML: A collection of longitudinal diabetes datasets for development of robust AI solutions
## Paper Abstract
Artificial intelligence (AI) algorithms are a critical part of state-of-the-art digital health technology for diabetes management. Yet, access to large high-quality datasets creates barriers that impede development of robust AI solutions. To accelerate development of transparent, reproducible, and robust AI solutions, we present Glucose-ML, a collection of 10 publicly available diabetes datasets, released within the last 7 years (i.e. 2018 - 2025). The Glucose-ML collection comprises over 300,000 days of continuous glucose monitor (CGM) data with a total of 38 million glucose samples, and was collected from 2500+ people, across 4 countries, living with type 1 diabetes, type 2 diabetes, prediabetes, and no diabetes. To support researchers and innovators with using this rich collection of diabetes datasets, we present a comparative analysis to guide algorithm developers with data selection, and to elicit strengths and weaknesses of each dataset. In addition, we conduct a case study focused on a common AI task within the field (i.e., blood glucose prediction). Through this study, we provide a benchmark for short-term blood glucose prediction across all 10 publicly available diabetes datasets within the Glucose-ML collection. We also show that the same algorithm can have significantly different prediction results when developed/evaluated with different datasets. Findings from this study are used to inform recommendations for developing robust AI solutions within the diabetes or broader health domain.

---

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

This repository is organized into the following folders:

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

## Preprocessing

To preprocess the datasets, navigate to the ```preprocessing_script/``` folder and follow the instructions in its [README](./preprocessing_script/README.md).

## Case Study: Blood glucose prediction

For baseline performance and blood glucose prediction case studies, refer to the ```baseline_performance/``` folder and its [README](./baseline_performance/README.md).

## Comparative Analysis

 ```Paper_Figures/``` includes the figuers presented in the paper. For the code to plot those figures and the tables included in the paper, please refer to the ```Script_for_Figures/``` and ```Script_for_Tables/```.

## License

This project is licensed under the MIT License.


