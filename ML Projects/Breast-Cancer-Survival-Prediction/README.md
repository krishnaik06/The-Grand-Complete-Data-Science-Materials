github: https://github.com/SujalNeupane9
linkedin: https://www.linkedin.com/in/sujal-neupane-2a9a2b210/

# Breast-Cancer-Survival-Prediction

## Overview
This repository contains code for predicting breast cancer survival using machine learning techniques. It includes a trained CatBoost model and preprocessing pipeline, along with scripts for data preprocessing, training, and a Streamlit app for model demonstration.

## Repository Structure
- **model:** Contains saved pickle files of the CatBoost model and the preprocessing pipeline.
- **src:** Includes scripts for different purposes:
  - `hyperparameters.py`: Defines hyperparameters used in the model.
  - `logger.py`: Logging functionalities for tracking the training process.
  - `preprocessing.py`: Preprocessing methods and functions.
  - `train.py`: Script for training the breast cancer survival prediction model.
  - `ingest_data.py`: Data ingestion and processing script.
- **notebook:** Experimental notebooks used for analysis and development.
- `run_pipeline.py`: Script to initiate the training process using the source code present in the `src` directory.
- `streamlit_app.py`: Streamlit application for demonstrating the functionality of the trained model.

## Usage
- **Training:** Use `run_pipeline.py` to execute the training process. Ensure necessary dependencies are installed by referring to the `requirements.txt` file.
- **Demo:** Run `streamlit_app.py` to launch the Streamlit app for demonstrating the trained model. Make sure to have the required libraries installed as mentioned in `requirements.txt`.

## Getting Started
1. Clone this repository.
2. Set up a Python environment and install the necessary dependencies listed in `requirements.txt`.
3. Utilize the provided scripts in the `src` directory for model training, data preprocessing, etc.
4. Execute the `run_pipeline.py` script to train the model.
5. Run the `streamlit_app.py` to experience the model via the Streamlit app.

## Contributions
Contributions are welcome! Feel free to fork this repository, make changes, and create a pull request. Please adhere to the repository's guidelines.

## License
This project is licensed under [MIT License](LICENSE).

