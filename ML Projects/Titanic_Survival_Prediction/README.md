# Titanic Survival Prediction

This project aims to predict the survival of passengers aboard the Titanic using a Logistic Regression model. The model is trained on a dataset of passenger information and can predict whether a passenger would survive based on user-provided input features.

## Project Structure

- `train.csv`: The dataset containing information about Titanic passengers.
- `titanic_survival_prediction.py`: The main Python script that preprocesses the data, trains the model, and predicts survival based on user input.

## Requirements

- Python 3.x
- numpy
- pandas
- scikit-learn

## Setup

1. Ensure you have Python 3.x installed on your system.
2. Install the necessary Python packages using pip:
    ```sh
    pip install numpy pandas scikit-learn
    ```

## Usage

1. Place the `train.csv` file in the same directory as `titanic_survival_prediction.py`.
2. Run the `titanic_survival_prediction.py` script:
    ```sh
    python titanic_survival_prediction.py
    ```
3. Follow the prompts to enter passenger details:
    - Passenger class (1st, 2nd, or 3rd)
    - Gender (Male/Female)
    - Age
    - Number of siblings or spouses aboard
    - Number of parents or children aboard
    - Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)
    - Fare

4. The model will predict whether the passenger would survive or not and display the model accuracy.

## Script Details

### Data Preprocessing

The following preprocessing steps are applied to the dataset:
- Drop the `Cabin` column due to a large number of missing values.
- Fill missing `Age` values with the mean age.
- Fill missing `Embarked` values with the mode.
- Fill missing `Fare` values with the mean fare.
- Convert categorical variables `Sex` and `Embarked` to numerical values.

### Model Training

- The features are defined by dropping irrelevant columns (`PassengerId`, `Name`, `Ticket`, `Survived`).
- The target variable is `Survived`.
- The dataset is split into training and testing sets (80-20 split).
- A Logistic Regression model is trained on the training set.

### Prediction Function

- Prompts the user for passenger details.
- Converts user input into a format suitable for the model.
- Predicts survival based on user input.
- Displays whether the passenger is predicted to survive or not.
- Prints the model's accuracy on the test set.

