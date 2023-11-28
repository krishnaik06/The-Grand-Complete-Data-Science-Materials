import os
import sys
import pandas as pd
from src.Heart.logger import logging
from src.Heart.utils.utils import load_object
from src.Heart.exception import customexception

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self,features):
        try:
            preprocessor_path=os.path.join("Artifacts","Preprocessor.pkl")
            model_path=os.path.join("Artifacts","Model.pkl")
            preprocessor=load_object(preprocessor_path)
            model=load_object(model_path)
            scaled_data=preprocessor.transform(features)
            pred=model.predict(scaled_data)
            return pred

        except Exception as e:
            raise customexception(e,sys)
    
class CustomData:
    def __init__(self,
                 age:int,
                 sex:int,
                 cp:int,
                 trestbps:int,
                 chol:int,
                 fbs:int,
                 restecg:int,
                 thalach:int,
                 exang:int,
                 oldpeak:float,
                 slope:int,
                 ca:int,
                 thal:int):
        
        self.age = age
        self.sex = sex
        self.cp = cp
        self.trestbps = trestbps
        self.chol = chol
        self.fbs = fbs
        self.restecg = restecg
        self.thalach = thalach
        self.exang = exang
        self.oldpeak = oldpeak
        self.slope = slope
        self.ca = ca
        self.thal = thal
            
                
    def get_data_as_dataframe(self):
            try:
                custom_data_input_dict = {
                    'age':[self.age],
                    'sex':[self.sex],
                    'cp':[self.cp],
                    'trestbps':[self.trestbps],
                    'chol':[self.chol],
                    'fbs':[self.fbs],
                    'restecg':[self.restecg],
                    'thalach':[self.thalach],
                    'exang':[self.exang],
                    'oldpeak':[self.oldpeak],
                    'slope':[self.slope],
                    'ca':[self.ca],
                    'thal':[self.thal]
                }
                df = pd.DataFrame(custom_data_input_dict)
                print(df)
                logging.info('Dataframe Gathered')
                return df
            except Exception as e:
                logging.info('Exception Occured in prediction pipeline')
                raise customexception(e,sys)
