
#Importing libraries
import numpy as np
import pandas as pd
import seaborn as sns
from tkinter import filedialog
import tkinter as tk
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score,roc_auc_score

class Teaching_Assistant(object):
    
    '''
        Use Case:Develop a Machine Learning Model that evaluates teaching performance scores :
        "low", "medium" or "high"
        Machine learning Model is created by using Random Forest Classifier
        Steps Followed for Building Random Forest Model:
        Step 1 : Loading dataset from the prompt:
                -The user is asked to select the input file
                -The user is allowed to load only  text file format as per current scenario
        Step 2 :Performing one-hot encoding:
                -One-hot encoding is performed on categorical features
        Step 3:Converting binary features into 0 and 1:
                -Binary features are converted into 0 and 1.
        Step 4: Performing feature Scaling on Numerical feature:
                -Min-max scaler is applied on numerical feature
        Step 5: Model Creation and Evaluation:
                -Model is created , accuracy and confusion matrix are calculated
            
        '''

    
    def __init__(self):
        
        '''
        The initialization method contains multiple functions:
        1. User is allowed to pass only the .txt files as input dataset.
        2. Feature's names are added to the dataset
        4. The method calls model_Creation_Evaluation()

        '''
        
        root = tk.Tk()
        root.withdraw()

        filename = filedialog.askopenfilename(title = "Select Text file",filetypes = (("TEXT Files","*.txt"),))
        data=pd.read_csv(filename,header = None)
        #adding features name to the data
        dataset=pd.DataFrame(data.values, columns = ["englishSpeaker", "CourseInstructor", "Course", "Semester","Classsize","grade"])
        categorical_feature=pd.DataFrame(dataset,columns={"CourseInstructor","Course"})
        binary_feature=pd.DataFrame(dataset,columns={"Semester","englishSpeaker"})
        self.model_Creation_Evaluation(dataset)
        
        
    def one_hot_encoding(self,dataset):
        
        '''
        One-hot encoding is performed on categorical features(CourseInstructor and Course)

        Parameters:
            data1 (pandas.core.frame.DataFrame):The input dataframe which is to be encoded. 
        
        returns: 
            encoded data for categorical features 
            
        '''
        course_ecoding_feature= pd.get_dummies(dataset.Course,prefix='Course',drop_first=True)
        courseInstructor_encoding_feature = pd.get_dummies(dataset.CourseInstructor, prefix='CourseInstructor',drop_first=True)
        combined_encoding_feature= pd.concat([course_ecoding_feature, courseInstructor_encoding_feature],axis=1)
        return combined_encoding_feature
        
    def converting_binary_feature(self,dataset):
        
        '''
        Binary features are handled by converting 1 as 0 and 2 as 1(englishSpeaker and Semester)

        Parameters:
            data1 (pandas.core.frame.DataFrame):The input dataframe which is to be handled. 
        
        returns: 
            encoded data for categorical features 
            
        '''
        binary_semester_feature=pd.DataFrame(dataset,columns={"Semester"})
        Semester1=[]
        for i in binary_semester_feature.Semester:
            if i==1:
                Semester1.append(0)
            else :
                Semester1.append(1)
        binary_semester_feature['Semester1']=Semester1
        binary_englishSpeaker_feature=pd.DataFrame(dataset,columns={"englishSpeaker"})
        englishSpeaker1=[]
        for i in binary_englishSpeaker_feature.englishSpeaker:
            if i==1:
                englishSpeaker1.append(0)
            else :
                englishSpeaker1.append(1)
        binary_englishSpeaker_feature['englishSpeaker1']=englishSpeaker1
        
        #Combining the dataframe
        combined_binary_feature= pd.concat([binary_semester_feature, binary_englishSpeaker_feature],axis=1)
        #taking englishSpeaker1 and Semester1
        filtered_combined_binary_feature=pd.DataFrame(combined_binary_feature,columns={"englishSpeaker1","Semester1"})
        one_hot_encoding_feature_filtered=self.one_hot_encoding(dataset)
        
        #combining the features
        combined_binary_categorical_feature=pd.concat([filtered_combined_binary_feature, one_hot_encoding_feature_filtered],axis=1)
        return combined_binary_categorical_feature
        
        
    def feature_Scaling(self,dataset):
        
        '''
        The columns in the dataframe are normalized within a range 0-1.
        
        Parameters:
            
            data1(pandas.core.frame.DataFrame):The dataframe containing the feature Classsize to be scaled. 
        
        returns: 
            scaled data for numerical features 
            
        '''
        #Storing the feature Classsize in a seperate dataframe
        filtered_classsize_feature=pd.DataFrame(dataset,columns={"Classsize"})
        sc= MinMaxScaler()
        classsize = sc.fit_transform(filtered_classsize_feature)
        scaled_filtered_classsize_feature=pd.DataFrame(classsize, columns=['classsize']) 
        both_combined_binary_numerical_feature=self.converting_binary_feature(dataset)
        final_prepared_feature_for_model=pd.concat([scaled_filtered_classsize_feature, both_combined_binary_numerical_feature],axis=1)
        return final_prepared_feature_for_model
    
    
    
    def model_Creation_Evaluation(self,dataset):
        
        '''
        Model is created by using Random Forest Classifier.
        
        Parameters:
            
            data1(pandas.core.frame.DataFrame):The dataframe is split into training and testing test. 
        
        returns: 
            Accuracy_score,Confusion matrix and Classification Report  of the model, 
            
        '''
        
        X=self.feature_Scaling(dataset)
        y=dataset['grade']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 0)
        classifier=RandomForestClassifier()
        classifier.fit(X_train,y_train)
        y_pred=classifier.predict(X_test)
        y_pred1=classifier.predict_proba(X_test)
        print("Accuracy_score: {}".format(accuracy_score(y_test,y_pred)))
        from sklearn.model_selection import cross_val_score
        from sklearn.metrics import classification_report, confusion_matrix
        print(confusion_matrix(y_test, y_pred))
        print("=== Classification Report ===")
        print(classification_report(y_test, y_pred))
       
        



#Creating object of class BHP_DEA()
teaching_Assistant = Teaching_Assistant()

#Used for class
#print(Teaching_Assistant.__doc__)
#Used for method
#help(Teaching_Assistant.__init__)
#help(Teaching_Assistant.one_hot_encoding)

