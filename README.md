# Glucose-ML: A collection of longitudinal diabetes datasets for development of robust AI solutions
## Paper Introduction
[Place holder for my abstract]

---

## Requirements

To set up the environment and install the required dependencies, follow these steps:

    Environment Setup:
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

## Stucture

This repository is organized into the following folders:

1. ```preprocessing_script/```
    Contains scripts for cleaning and preparing raw datasets for analysis. 

2. ```Data_filter_70_coverage/```
    Includes scripts for filtering CGM data to retain days with at least 70% CGM data coverage. 
3. ```baseline_performance/```
    Contains scripts and results for baseline blood glucose prediction models. 
4. ```Paper_Figures/```
    Includes figures and visualizations used in the paper for comparison and analysis.

5. ```Script_for_Figures/```
    Include the Jupyter notebook files to calculate the plot the figures included in the paper.

6. ```Script_for_Tables/```
    Include the Jupyter notebook files to calculate the data for the tables included in the paper.

## Preprocessing

To preprocess the datasets, navigate to the ```preprocessing_script/``` folder and follow the instructions in its [README](./preprocessing_script/README.md).

## Case Study: Blood glucose prediction

For baseline performance and blood glucose prediction case studies, refer to the ```baseline_performance/``` folder and its [README](./baseline_performance/README.md).

## Compare and Analysis

 ```Paper_Figures/``` includes the figuers discussed in the paper. For the code to plot those figures and the tables include in the paper, please refer to the ```Script_for_Figures/``` and ```Script_for_Tables/```.

## License

This project is licensed under the MIT License.


