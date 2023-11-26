# Reducing-Credit-Default-Rate-at-Bank-
# Goal: 
* Finding out the risky customers using data, identify the characteristics and recommend suitable actions which will help the bank      reduce overall default rate.
# Background
* ABC Bank is facing the challenge of high credit default rates. 
* One of the strategies which the bank has come up with is to identify the risky customers (those who are likely to default) and take   proactive measures to perform actions for these risky customers before they actually default. .
#  Methodology-Solution Approach
Steps Followed for Building Machine Learning  Model:

Step 1: Loading the dataset

			-The dataset is loaded using python
      
			-Missing values, information regarding each features are being checked.
      
Step 2 :Preprocessing and Feature Engineering:

			-Distribution of the class is checked(Here dataset is imbalance)
      
			-Numerical and categorical features are selected from the dataset.
      
			-EDA is performed on both numerical and categorical dataset
      
			-Importance features are selected. I have used extra tree regressor and correlation matrix for feature importance for numerical features.
      
			-Finally feature scaling is performed on numerical features(Here I have used standardscaler)
      
			-Categorical features are selected based on domain knowledge
      
Step 3 :Performing one-hot encoding on categorical features

			-One-hot encoding is performed on categorical features and dummy variable trap is handled.
      
Step 4:Handling Imbalance dataset:

			-Since the dataset is imbalance ,SMOTE method is performed to balance the dataset.

Step 5: Model Creation:

		-Both numerical and categorical encoded features are combined and splitted the data into train and test split
    
		-Logistic regression,Decision tree ,Random forest and Xgboost algorithms are used create the model.

Step 5 :Model Evaluation:

		-accuracy,precision ,recall and f1-score are calculated and compared among all the models.
# Modeling Techniques Details
* Logistic Regression,Decision Tree,Random Forest and XGBoost algorithms are used to create model.
* More details regarding models can be found in the PPT and Jupyter notebook.
# Code Execution Steps
* Download the dataset(data.xlsx) and code.ipynb
* Execute code.ipynb and you can see the result in the notebook.
* For your reference ,you can find the analyis and model result in the PPT(Analysis_Result_Sakil.pptx)
