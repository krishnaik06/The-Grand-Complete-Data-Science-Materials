# Predicting-Heart-Disease-with-Support-Vector-Machines

**Step 1: Data Loading and Exploration**

- Import the neccessary libraries
- Load the heart disease dataset into a Pandas DataFrame.
- Explore the data using methods like head(), info(), and describe() to understand its structure and characteristics.

**Step 2: Exploratory Data Analysis (EDA)**

- Conduct exploratory data analysis to gain insights into the data's distribution and relationships.
- Visualize data using histograms, scatter plots, and correlation matrices.
- Identify patterns and potential insights related to heart disease diagnosis.

![Img](https://github.com/abhamidi-1234/Predicting-Heart-Disease-with-Support-Vector-Machines/blob/main/Capture1.PNG)

**Step 3: Data Preprocessing**

- Handle missing values, if any, by imputing or removing them.
- Encode categorical variables using one-hot encoding or label encoding.
-Remove unnecessary columns that won't be used in the SVM model.

**Step 4: Feature Selection**

- Choose relevant features for predicting heart disease.
- Consider the impact of each feature on the prediction task.
- Decide whether to use all features or a subset based on domain knowledge.

**Step 5: Data Splitting**

- Split the dataset into training and testing sets to evaluate the model's performance.
- Common splits include 70-30 or 80-20 for training and testing, respectively.

**Step 6: Feature Scaling**

- Standardize or normalize the feature values to ensure they are on the same scale.
- Scaling is essential for SVM as it relies on distances between data points.

The **Radial Basis Function (RBF)** that we are using with our **Support Vector Machine** assumes that the data are centered and scaled, so we need to do this to both the training and testing datasets.

**NOTE:** We split the data into training and testing datasets and then scale them separately to avoid **Data Leakage**. **Data Leakage** occurs when information about the training dataset currupts or influences the testing dataset.

**Step 7: SVM Model Building**

- Create an SVM model for classification.
- Choose the appropriate SVM kernel (e.g., linear, polynomial, or radial basis function).
- Initialize the model with hyperparameters like C (regularization parameter) and kernel-specific parameters.

**Step 8: Model Training**

- Train the SVM model on the training data.
- The model learns to differentiate between patients with and without heart disease based on the features.

**Step 9: Model Evaluation**

- Evaluate the SVM model's performance on the testing data:
- Calculate classification metrics such as accuracy, precision, recall, F1-score, and the confusion matrix.
- Visualize results through ROC curves and precision-recall curves.
- Use cross-validation for robust model evaluation.

**Step 10: Hyperparameter Tuning**

- Optimize the SVM model's hyperparameters (Gamma, C and kernel parameters) using techniques like grid search or random search to improve model performance.

**Step 11: Interpretation of Results**

- Interpret the SVM model's findings
- Identify the most influential features for heart disease prediction.
- Understand the decision boundaries and support vectors in the SVM model.

![Img](https://github.com/abhamidi-1234/Predicting-Heart-Disease-with-Support-Vector-Machines/blob/main/Capture2.PNG)

![Img](https://github.com/abhamidi-1234/Predicting-Heart-Disease-with-Support-Vector-Machines/blob/main/Capture3.PNG)

![Img](https://github.com/abhamidi-1234/Predicting-Heart-Disease-with-Support-Vector-Machines/blob/main/Capture4.PNG)

**Step 12: Conclusion and Insights**

- Summarize findings and insights from the heart disease prediction analysis.
- Provide actionable recommendations for healthcare or patient management based on the SVM model's predictions.


## How to reach me

https://www.linkedin.com/in/abhishek-bhamidipati/

https://abhishekcmu.wixsite.com/home

https://github.com/abhamidi-1234