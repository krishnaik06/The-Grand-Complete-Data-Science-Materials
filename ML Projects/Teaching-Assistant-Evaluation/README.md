# Teaching-Assistant-Evaluation Using different ML and DL Techniques
# Highlights
* Different ML and DL model have been implemented and the results are compared.
* Machine learning skills
* Analysis and Presenting the result(Please refer ML_case_studysakil_Analysis_result.pptx)
* Coding standard: I have followed object-oriented approach and also used docstring for commenting the code(Please refer Model_Creation_using_Random_forest_using_OOP file).
# Information Regarding Files
* ML_case_studysakil_Analysis_result.pptx: Detailed analysis result,model result ,approach ,architecture diagram
* ML_Case_Study_solution.zip: Includes all the python script of the use case
* Userguide.pdf: Information regarding the files in ML_Case_Study_solution.zip
* requirements.txt: libraries to be installed to execute the script.

# Goal
Develop a Machine Learning Model that evaluates teaching performance scores : "low", "medium" or "high".

# Background
* The quality of teaching assistants’ work is important to students' education and inclusion, so it is of significance to evaluate and improve the performance of teaching assistants.  
* The teaching assistant evaluation reviews academic qualifications, relevant experience, quality of teaching, and professional contributions. 
* All aspects can be assessed by the students, peers or by the teachers themselves. 
* The project focuses on the application of some machine learning techniques on the data in order to develop a model that can use some past assessment to determine a future evaluation.

# Attribute Information
* Whether of not the TA is a native English speaker (binary); 1=English speaker, 2=non-English speaker
* Course instructor (categorical, 25 categories)
* Course (categorical, 26 categories)
* Summer or regular semester (binary) 1=Summer, 2=Regular
*  Class size (numerical)
*  Class attribute (categorical) 1=Low, 2=Medium, 3=High

# Dataset & Attribute Information
## Dataset
* The data consist of evaluations of teaching performance over three regular semesters and two summer semesters of 151 teaching assistant (TA) assignments at the Statistics Department of the University of Wisconsin-Madison.
* The scores were divided into 3 roughly equal-sized categories ("low", "medium", and "high") to form the class variable.

## Data Attribute Overview 
* Data Set Characteristics--------Multivariate
* Number of Instances-------------151
* Attribute Characteristics----Categorical, Integer
* Number of Attributes--------5
* Associated Tasks-----------Classification
# Dataset Preparation
* The data was given in text format with no header.
* The header is added in the dataset (for more detail refer to PPT attached)
# Dataset
* Please refer to the PPT attahced for getting information regarding dataset
# Exploratory Data Analysis
* Please refer to the PPT attahced.
# Preprocessing and Feature Engineering 
* The quality of data is checked. The data has no missing value
* The data has two categorical features:CourseInstructor and course.
* CourseInstructor has 25 categories
* Course has  26 categories
# Feature Engineering
## Handling Categorical Features
* The categorical features are handeled in following two  ways:
1. One hot encoding
2. One-hot encoding on 10 most frequent categories.
# Preprocessing and Feature Engineering 
* One hot encoding is performed on CourseInstructor and Course.
* Dummy variable trap is handled.
* We have 52 independent features.
* Binary features Semester and englishInstructor are handled by replacing 1 as 0 and 2 as 1.
# One-hot encoding on 10 most frequent categories 
* Top 10 most frequent features are taken and one hot encoding is performed and kept 0 for remaining features.
* The feature is handled and accuracy is compared.
* For more detail, please refer the PPT.
# Normalization
* Input attribute (Class size-numerical) has numerical values that can be very distant from each other.
* To prevent that we will normalize data set using Max-Min normalization and standardization.
* The accuracy of the model doesn’t change much even after using standard scaler.
# Model Creation
* Various Machine learning algorithms are developed, and accuracy is compared.
* An artificial Neural (ANN)Algorithm is also performed though the data is very small. 
* Randomized Search Cv and grid search are used for hyperparameter optimization.
* Used auto-ml tool pycaret to compare the accuracy.
* Precision, recall and F1 score are used as metrics.
# Model Accuracy Result
* The model is trained on 80% and 90% of the data and the accuracy is compared
* Please refer to the PPT for more details regarding model accuracy.
# Challenges, Future work and Conclusion
* Analysis for  the data is performed and 87.5% accuracy is achieved. 
* The accuracy of the algorithm can be increased by increasing data.
* Machine learning and deep learning algorithms are developed, and the accuracy is compared. 
* The model created by auto ml gives less accuracy than the model created by machine learning.
* The dataset was too small and also had too many categories in the categorical features which lead to difficulty in deciding which algorithm to choose.

# Note:
* For code execution ,please follow the user guide attached.

