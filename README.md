# Python QT6 UI app 
Program, developed for Masters Dissertation project, dedicated to use of synthetic images in wildfire detection via CNN and easier monitoring

*Test text

## Preparations
### 1) You need Python 3.13 or higher with pip
### 2) Install additional packages from "project_dependencies.txt" with
    pip install -r project_dependencies.txt
### 3) Download 2 .keras neural networks from this Kaggle repository:
    text
### 3.5) If you are interested, you can see the synthetic dataset, used to train the model in there as well:
    link here
### 4) Create folders in the same path as all files (main, LoadAiModels, etc)
### so that i looks like this: /neural_networks/Image Model/
### Then add downloaded image classification model, so that full path will look like this:
    /neural_networks/Image Model/Models/wildfire_image_classification_v1_local.keras
### 5) Do the same for: /neural_networks/Numeric Model/
### In the end for FNN model the path should look like this:
    /neural_networks/Numeric Model/Weather_parameters_model_firebias_v1.keras
