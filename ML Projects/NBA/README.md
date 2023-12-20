# Project Presentation:
The goal is to create a classification system that can predict whether a basketball player deserves investment by anticipating if they will remain in the NBA for more than five years based on their sports performance. This model aims to provide guidance to investors looking to capitalize on the potential of future NBA talents.

# File Structure:
The project is divided into several main files:

- **artifacts:** This folder stores data before and after preprocessing, as well as training and testing sets, and models found, saved as Joblib files.
- **schema.yaml:** This YAML file contains the features used for predictions. These features were selected based on their importance in the model.
- **params.yaml:** It contains the parameters of the machine learning model.
- **app.py:** This file contains the endpoints of the Flask application.
- **main.py:** This file is used to launch the pipeline scripts.
- **logs:** Contains logs during code execution.
- **static:** File containing CSS and JS scripts.
- **templates:** File containing HTML code for the form and prediction interface.
- **research:** You will find a file named "Exploration.ipynb." This notebook compiles all the steps of the problem modeling as well as the decisions made during the process.
- **demo_app.mkv:** A demonstration of the application.

# How to Launch the Application?

### Step 01: Create a Virtual Environment

- ```python -m venv env```
- ```env\Scripts\activate```

### Step 02: Install Requirements

- ```pip install -r requirements.txt```
- ```python app.py```