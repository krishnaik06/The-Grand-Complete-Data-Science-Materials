# README: SVM vs XGBoost Classifier vs Sequential Nueral Net

## Overview
This project compares the performance of Support Vector Machine (SVM) and XGBoost classifiers and Nueral Networks for predicting income levels based on demographic features.

## Dataset

- **File:** `applicant.csv`
- **Features:** Age, work class, education, marital status, occupation, etc.
- **Target Variable:** Income (>50K, <=50K)

## Exploratory Data Analysis (EDA)

- Checked for duplicates and null values (none found).
- Analyzed target distribution, identifying a class imbalance.
- Explored age's relationship with income through histograms.
- Visualized selected categorical features.

## Data Preprocessing

- Encoded categorical columns: Gender, Occupation, Relationship, Target.
- Selected features: Gender, Occupation, Relationship, Education-Num, Age.

## Models

1. **Support Vector Machine (SVM):**
   - Trained a linear SVM model.
   - Test Accuracy: 80.7%

2. **XGBoost Classifier:**
   - Hyperparameter tuning with GridSearchCV.
   - Test Accuracy: 82.59%

3. **Sequential Neural Network:**
   - Implemented a neural network with two hidden layers 'tanh' activation function in the hidden layer.
   - Test Accuracy: 82.67%

## Conclusion

- Sequential Neural Network and XGBoost Classifier outperformed SVM.
- **Best Accuracy:** Sequential Neural Network - 82.67%
- Explore and modify the code for your datasets and experiments!
## Contribution 
- [Kaif khan]
