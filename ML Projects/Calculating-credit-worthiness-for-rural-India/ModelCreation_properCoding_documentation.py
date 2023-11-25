
#Importing libraries
import numpy as np
import pandas as pd
import seaborn as sns
from tkinter import filedialog
import tkinter as tk
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
class Calculating_Credit_Worthiness(object):
    '''
        Use Case:Performing descriptive analysis of the features of the data and understanding  the maximum repayment capability of customers 
        which can be used to grant them the desired amount
        Machine learning Model is created by using Random Forest Regressor
        Steps Followed for Building Random Forest Model:
        Step 1 : Loading dataset from the prompt:
                -The user is asked to select the input file
                -The user is allowed to load only  CSV file format as per current scenario
        Step 2: Handling missing values:
                -Mode is used for handling categorical missing value and mean is used for numerical value.
        Step 3 :Performing one-hot encoding:
                -One-hot encoding is performed on categorical features:sex and type_of_house
        Step 4:Converting loan_purpose features into 0 and 1:
                -Top 10 most frequent categories in loan_purpose features are taken 
                and one hot encoding is performed and the remaining categories are placed with 0..
        Step 5: Model Creation and Evaluation:
                -Model is created , accuracy and MSE,MAE and RMSE are calculated
            
        '''
    def __init__(self):
        '''
        The initialization method contains multiple functions:
        1. User is allowed to pass only the .csv files as input dataset.
        2. The method calls model_Creation_Evaluation()

        '''
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(title = "Select Text file",filetypes = (("CSV Files","*.csv"),))
        data=pd.read_csv(filename)
        categorical_feature=pd.DataFrame(data,columns={"type_of_house","sex"})
        self.model_Creation_Evaluation(data)
    def handling_missing_value(self,data):
        i = data[(data.age ==205)].index
        j=data[(data.age==288)].index
        k=data[(data.age==766105)].index
        #deleting three records
        data_updated1=data.drop(i)
        data_updated2=data.drop(j)
        data_updated2=data.drop(k)
        data_updated3=data_updated2.copy()
        #Handling missing values with mean and mode
        data_updated3['social_class']=data_updated3['social_class'].fillna(data_updated3['social_class'].mode()[0])
        data_updated3['city']=data_updated3['city'].fillna(data_updated3['city'].mode()[0])
        data_updated3['primary_business']=data_updated3['primary_business'].fillna(data_updated3['primary_business'].mode()[0])
        data_updated3['secondary_business']=data_updated3['secondary_business'].fillna(data_updated3['secondary_business'].mode()[0])
        data_updated3['type_of_house']=data_updated3['type_of_house'].fillna(data_updated3['type_of_house'].mode()[0])
        data_updated3['sanitary_availability']=data_updated3['sanitary_availability'].fillna(data_updated3['sanitary_availability'].mode()[0])                                                      
        data_updated3['water_availabity']=data_updated3['water_availabity'].fillna(data_updated3['water_availabity'].mode()[0])
        data_updated3['loan_purpose']=data_updated3['loan_purpose'].fillna(data_updated3['loan_purpose'].mode()[0])
        data_updated3['monthly_expenses']=data_updated3['monthly_expenses'].fillna(data_updated3['monthly_expenses'].mean())
        data_updated3['home_ownership']=data_updated3['home_ownership'].fillna(data_updated3['home_ownership'].mode()[0])
        return data_updated3
    def one_hot_encoding(self,data):
        data=self.handling_missing_value(data)
        type_of_house_ecoding_feature= pd.get_dummies(data.type_of_house,prefix='type_of_house',drop_first=True)
        sex_encoding_feature = pd.get_dummies(data.sex, prefix='sex',drop_first=True)
        combined_encoding_feature= pd.concat([type_of_house_ecoding_feature, sex_encoding_feature],axis=1)
        return combined_encoding_feature
    def handling_loanpurpose_feature(self,data):
        '''
        Missing value is performed on the features using mode and mean.

        Parameters:
            data (pandas.core.frame.DataFrame):The input dataframe which is to be encoded. 
        
        returns: 
            missing handled data for features 
            
        '''
        data=self.handling_missing_value(data)
        kdddata1=pd.DataFrame(data,columns={"loan_purpose"})
        #print top 10 features for loan_purpose
        loan_purpose_10=kdddata1.loan_purpose.value_counts().sort_values(ascending=False).head(10).index
        loan_purpose_10=list(loan_purpose_10)
        import numpy as np
        for categories in loan_purpose_10:
            kdddata1[categories]=np.where(kdddata1['loan_purpose']==categories,1,0)
        kdddata1.head()
        kdddata1 = kdddata1.add_suffix('loan_purpose')
        combined_encoding_feature_data=self.one_hot_encoding(data)
        features=pd.concat([kdddata1, combined_encoding_feature_data],axis=1)
        features1=features.drop(['loan_purposeloan_purpose'], axis = 1) 
        return features1
    def feature_ready(self,data):
        '''
        All features are combined and made ready for the model creation.

        Parameters:
            data (pandas.core.frame.DataFrame):The input dataframe which is to be encoded. 
        
        returns: 
            ready features 
            
        '''
        
        one_hot_loan_combined_features=self.handling_loanpurpose_feature(data)
        datax=self.handling_missing_value(data)
        data_XY=pd.DataFrame(datax,columns={"Id","age","annual_income",
                                     "monthly_expenses","old_dependents","young_dependents","home_ownership",
                                     "occupants_count","house_area","loan_tenure","loan_installments","loan_amount"})
        
        final_features=pd.concat([data_XY, one_hot_loan_combined_features],axis=1)
        return final_features
    def model_Creation_Evaluation(self,data):
        '''
        Model is created by using Random Forest Classifier.
        
        Parameters:
            
            data1(pandas.core.frame.DataFrame):The dataframe is split into training and testing test. 
        
        returns: 
            MAE,MSE,RMSE ,actual vs predicted graphand accuracy of the model, 
            
        '''
        ready_features=self.feature_ready(data)
        from sklearn import metrics
        y=pd.DataFrame(ready_features,columns={"loan_amount"})
        X=ready_features.drop(['loan_amount'], axis = 1) 
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
        from sklearn.ensemble import RandomForestRegressor
        randomforest=RandomForestRegressor()
        randomforest.fit(X_train,y_train)
        randomforest_prediction=randomforest.predict(X_test)
        randomforest_prediction_data=pd.DataFrame(randomforest_prediction,columns={"Predicted_loan_amount"})
        y_test1=y_test.copy()
        y_test1=y_test1.reset_index()
        y_test2=pd.DataFrame(y_test1,columns={"loan_amount"})
        df_row_merged_randomforest = pd.concat([randomforest_prediction_data,y_test2],axis=1)
        df_row_merged_randomforest[['loan_amount','Predicted_loan_amount']].plot()
        print('MAE:', metrics.mean_absolute_error(y_test, randomforest_prediction))
        print('MSE:', metrics.mean_squared_error(y_test, randomforest_prediction))
        print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, randomforest_prediction)))
        df_row_merged_randomforest['error_rate']=(abs(df_row_merged_randomforest['loan_amount']-df_row_merged_randomforest['Predicted_loan_amount'])/df_row_merged_randomforest['loan_amount'])*100
        #mean error rate
        mean_error=df_row_merged_randomforest.error_rate.mean()
        #calculating accuracy
        accuracy=100-mean_error
        print("<<<The accuracy is >>>")
        print(accuracy)
#Creating object of class Calculating_Credit_Worthiness()
calculating_Credit_Worthiness = Calculating_Credit_Worthiness()
#print(Calculating_Credit_Worthiness.__doc__)
#help(Calculating_Credit_Worthiness.__init__)

