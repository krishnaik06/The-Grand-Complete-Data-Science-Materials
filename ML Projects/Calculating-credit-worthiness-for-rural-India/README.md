# Calculating-credit-worthiness-for-rural-India-

# Goal: 

* Performing descriptive analysis of the features of the data and understanding  the maximum repayment capability of customers which can   be used to grant them the desired amount
# Background:
* In Banking industry, loan applications are generally approved after a thorough background
   check of the customer's repayment capabilities.
* Credit Score plays a significant role in identifying customer's financial behaviour (specifically default).
* People belonging to rural India do not have credit score and it is difficult to do a direct assessment.
# Attribute Information
1. Id: Primary Key
2. Personal Details: city, age, sex, social_class
3. Financial Details: primary_business, secondary_business, annual_income, monthly_expenses,
old_dependents, young_dependents
4. House Details: home_ownership, type_of_house, occupants_count, house_area, sanitary_availability,water_availability
5. Loan Details: loan_purpose, loan_tenure, loan_installments, loan_amount (these contain loan details of loans that have been     previously given, and which have been repaid)
 # Solution Approach
 Steps Followed for Building Machine Learning  Model:
 
Step 1: Loading the dataset from the  prompt
			-The user is asked to select the input file
			-The user is allowed to load only  CSV file format as per current scenario

Step 2 :Handling missing values
			-Mode is used for handling categorical missing value and mean is used for numerical value.
      
Step 3 :Performing one-hot encoding
			-One-hot encoding is performed on categorical features:sex and type_of_house
      
Step 4:Converting loan_purpose features into 0 and 1:
			-Top 10 most frequent categories in loan_purpose features are taken and one hot encoding is performed and the remaining categories are placed with 0.
      
Step 5 :Model Creation and Evaluation:
		-Model is created , accuracy and MSE,MAE and RMSE are calculated
# Code Execution Steps:
* Two python scripts files are present: EDA and Model creation.ipynb and ModelCreation_properCoding_documentation.py.
* EDA and Model creation.ipynb files has all EDA and Model creation scripts.
* ModelCreation_properCoding_documentation.py: I have followed object oriented programming approach for creating model.For this usecase,Random Forest gives good accuracy.
# Note
* I have kept all the analysis results, approach in the PPT:Detailed_Analysis_result_Sakil.pptx
# Note 
* trainingData .csv: I have used this dataset for the use case.
