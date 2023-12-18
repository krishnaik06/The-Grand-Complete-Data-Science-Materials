# Stack Overflow: Tag Prediction


#  Business Problem
##  Description

Description

Stack Overflow is the largest, most trusted online community for developers to learn, share their programming knowledge, and build their careers.

Stack Overflow is something which every programmer use one way or another. Each month, over 50 million developers come to Stack Overflow to learn, share their knowledge, and build their careers. It features questions and answers on a wide range of topics in computer programming. The website serves as a platform for users to ask and answer questions, and, through membership and active participation, to vote questions and answers up or down and edit questions and answers in a fashion similar to a wiki or Digg. As of April 2014 Stack Overflow has over 4,000,000 registered users, and it exceeded 10,000,000 questions in late August 2015. Based on the type of tags assigned to questions, the top eight most discussed topics on the site are: Java, JavaScript, C#, PHP, Android, jQuery, Python and HTML.

Problem Statemtent
Suggest the tags based on the content that was there in the question posted on Stackoverflow.

Source: https://www.kaggle.com/c/facebook-recruiting-iii-keyword-extraction/
##  Source / useful links

Data Source : https://www.kaggle.com/c/facebook-recruiting-iii-keyword-extraction/data
Youtube : https://youtu.be/nNDqbUhtIRg
Research paper : https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tagging-1.pdf
Research paper : https://dl.acm.org/citation.cfm?id=2660970&dl=ACM&coll=DL
## Real World / Business Objectives and Constraints

    Predict as many tags as possible with high precision and recall.
    Incorrect tags could impact customer experience on StackOverflow.
    No strict latency constraints.

#  Machine Learning problem
##  Data
###  Data Overview

Refer: https://www.kaggle.com/c/facebook-recruiting-iii-keyword-extraction/data
All of the data is in 2 files: Train and Test.

Train.csv contains 4 columns: Id,Title,Body,Tags.

Test.csv contains the same columns but without the Tags, which you are to predict.

Size of Train.csv - 6.75GB

Size of Test.csv - 2GB

Number of rows in Train.csv = 6034195

The questions are randomized and contains a mix of verbose text sites as well as sites related to math and programming. The number of questions from each site may vary, and no filtering has been performed on the questions (such as closed questions).

Data Field Explaination

Dataset contains 6,034,195 rows. The columns in the table are:

Id - Unique identifier for each question

Title - The question's title

Body - The body of the question

Tags - The tags associated with the question in a space-seperated format (all lowercase, should not contain tabs '\t' or ampersands '&')




## Mapping the real-world problem to a Machine Learning Problem
###  Type of Machine Learning Problem

It is a multi-label classification problem
Multi-label Classification: Multilabel classification assigns to each sample a set of target labels. This can be thought as predicting properties of a data-point that are not mutually exclusive, such as topics that are relevant for a document. A question on Stackoverflow might be about any of C, Pointers, FileIO and/or memory-management at the same time or none of these.
__Credit__: http://scikit-learn.org/stable/modules/multiclass.html
### Performance metric

Micro-Averaged F1-Score (Mean F Score) : The F1 score can be interpreted as a weighted average of the precision and recall, where an F1 score reaches its best value at 1 and worst score at 0. The relative contribution of precision and recall to the F1 score are equal. The formula for the F1 score is:

F1 = 2 * (precision * recall) / (precision + recall)

In the multi-class and multi-label case, this is the weighted average of the F1 score of each class.

'Micro f1 score':
Calculate metrics globally by counting the total true positives, false negatives and false positives. This is a better metric when we have class imbalance.

'Macro f1 score':
Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.

https://www.kaggle.com/wiki/MeanFScore
http://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html

Hamming loss : The Hamming loss is the fraction of labels that are incorrectly predicted.
https://www.kaggle.com/wiki/HammingLoss
##  Exploratory Data Analysis
## Data Loading and Cleaning
### Using Pandas with SQLite to Load the data
### Counting the number of rows 

###  Checking for duplicates

##  Analysis of Tags
### Total number of unique tags
### Number of times a tag appeared 


Observations:

    1.There are total 153 tags which are used more than 10000 times.
    2.14 tags are used more than 100000 times.
    3.Most frequent tag (i.e. c#) is used 331505 times.
    4.Since some tags occur much more frequenctly than others, Micro-averaged F1-score is the appropriate metric for this probelm.

###  Tags Per Question


Observations:

    1.Maximum number of tags per question: 5
    2.Minimum number of tags per question: 1
    3.Avg. number of tags per question: 2.899
    4.Most of the questions are having 2 or 3 tags
###  Most Frequent Tags 
Observations:
A look at the word cloud shows that "c#", "java", "php", "asp.net", "javascript", "c++" are some of the most frequent tags
###  The top 20 tags 


Observations:

    Majority of the most frequent tags are programming language.
    C# is the top most frequent programming language.
    Android, IOS, Linux and windows are among the top most frequent operating systems.

##  Cleaning and preprocessing of Questions
### Preprocessing

    Sample 1M data points
    Separate out code-snippets from Body
    Remove Spcial characters from Question title and description (not in code)
    Remove stop words (Except 'C')
    Remove HTML Tags
    Convert all the characters into small letters
    Use SnowballStemmer to stem the words


# Machine Learning Models
##  Converting tags for multilabel problems
We will sample the number of tags instead considering all of them (due to limitation of computing power) 


We consider top 15% tags which covers 99% of the questions
## Split the data into test and train (80:20)
##  Featurizing data 
##  Applying Logistic Regression with OneVsRest Classifier
Accuracy : 0.254075
Hamming loss  0.0026348
Micro-average quality numbers
Precision: 0.7746, Recall: 0.5370, F1-measure: 0.6343
Macro-average quality numbers
Precision: 0.2615, Recall: 0.1673, F1-measure: 0.1787
##  Linear SVM with OneVsRestClassifier
Accuracy : 0.226225
Hamming loss  0.00282655
Micro-average quality numbers
Precision: 0.7244, Recall: 0.5418, F1-measure: 0.6199
Macro-average quality numbers
Precision: 0.1883, Recall: 0.1740, F1-measure: 0.1575

# Conclusion

1.We have choosen 'f1_micro' scoring metric because of the stated business statement.

2.Used bag of words upto 4 grams.

3.For logistic regression , I have used 'SGDClassifier' instead of 'LogisticRegression'. The reason is 'LogisticRegression' takes lots of time for hyperparameter tuning. Even we have not choosen any complex model like xgboost, because the dimension is very high and linear model works fairly well in high dimension and the complex model like xgboost may not work well for this much high dimension, as well as it takes lots of time for hyperparameter tuning


