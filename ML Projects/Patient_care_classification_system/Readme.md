# Patient Care Classification System

This project focuses on classifying patients into two categories: "In Care" and "Out Care." The classification is based on various health indicators provided in the dataset. The machine learning models used for classification include Decision Tree, Random Forest, and Logistic Regression.


## Dataset
The dataset, named "PatientCare.csv," contains information about patients, including their gender, age, and various health parameters such as HAEMATOCRIT, HAEMOGLOBINS, ERYTHROCYTE, LEUCOCYTE, THROMBOCYTE, MCH, MCHC, and MCV.

## Preprocessing
The gender information is mapped to numerical values (1 for Male, 0 for Female) to facilitate model training. Exploratory Data Analysis (EDA) is performed to visualize the distribution of data using count plots and distribution plots.

## Model Training
The dataset is split into training and testing sets, and three machine learning models are trained: Decision Tree, Random Forest, and Logistic Regression. The accuracy of each model is evaluated using the test set.

## Streamlit Application
A Streamlit application is created to allow users to input their health parameters. The trained Random Forest model then predicts whether the user requires "In Care" (Hospitalization) or "Out Care" (Home Care). The user input and the model's prediction are displayed in the application.

## Instructions for Running the Streamlit App
1. Install the required Python libraries: `numpy`, `pandas`, `matplotlib`, `seaborn`, `streamlit`, and `scikit-learn`.
2. Clone the repository.
3. Navigate to the project directory in the terminal.
4. Run the Streamlit app using the command: `streamlit run your_streamlit_app_filename.py`.

## Note
- The models' performance metrics, including confusion matrices and classification reports, are provided in the Jupyter notebook.
- Make sure to have the necessary datasets in the specified file path.
- Adjustments to the dataset path or other parameters may be needed based on your local environment.

Feel free to explore and enhance the project further based on your requirements.



## Author 
[LinkedIn Profile](https://www.linkedin.com/in/yashpurusharthi/)
