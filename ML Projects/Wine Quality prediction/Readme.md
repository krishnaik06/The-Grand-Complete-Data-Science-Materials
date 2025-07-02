# 🍷 Wine Quality Prediction using Machine Learning

This project focuses on predicting the quality of wine based on its physicochemical features using machine learning algorithms. The dataset is sourced from the UCI Machine Learning Repository and includes red or white wine samples, with a quality score ranging from 0 to 10.

## 📌 Problem Statement

Given various features of wine such as acidity, sugar content, pH, and alcohol level, the goal is to build a regression/classification model that can predict the quality score of a wine sample.

---

## 📁 Dataset

- Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/wine+quality)
- Format: CSV
- Features include:
  - Fixed acidity
  - Volatile acidity
  - Citric acid
  - Residual sugar
  - Chlorides
  - Free sulfur dioxide
  - Total sulfur dioxide
  - Density
  - pH
  - Sulphates
  - Alcohol
  - Quality (target variable)

---

## 🛠️ Technologies Used

- Python
- Pandas & NumPy
- Matplotlib & Seaborn (for EDA and visualization)
- Scikit-learn (for modeling)
- Jupyter Notebook or Google Colab

---

## 🔍 Exploratory Data Analysis (EDA)

- Checked for null values
- Visualized feature distributions and correlations
- Analyzed class imbalance in the target variable

---

## ✅ Model Building

You can choose between Regression or Classification:
- **Regression Models:** Linear Regression, Random Forest Regressor, Gradient Boosting Regressor
- **Classification Models:** Logistic Regression, Random Forest Classifier, SVM, XGBoost

### Model Evaluation Metrics
- Regression: MAE, MSE, RMSE, R² Score
- Classification: Accuracy, Precision, Recall, F1 Score, Confusion Matrix

---

## 📊 Results

- Best performing model: `RandomForestClassifier` (for classification) or `GradientBoostingRegressor` (for regression)
- Achieved accuracy or R² score of approximately **⟨your score here⟩**

---

