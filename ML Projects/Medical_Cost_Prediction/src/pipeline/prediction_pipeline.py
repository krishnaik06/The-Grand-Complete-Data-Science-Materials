import sys
import os
import pandas as pd
from src.exception import CustomException
from src.utils import load_object

class PreditctPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = os.path.join("artifacts","model.pkl")
            preprocessor_path = os.path.join("artifacts","preprocessor.pkl")

            model = load_object(file_path = model_path)
            preprocessor = load_object(file_path = preprocessor_path)

            print(model)
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        except Exception as e:
            raise CustomException(e, sys)
        
# numerical_features = ['children']
#             categorical_features = ['age_range', 'bmi_range', 'sex', 'smoker', 'region']
class InputData:
    def __init__(self,
        age: int,
        children: int,
        bmi: float,
        sex: str,
        smoker: str,
        region: str):

        self.age = age
        self.children = children
        self.bmi = bmi
        self.sex = sex
        self.smoker = smoker
        self.region = region

    def get_data_as_dataFrame(self):
        try:
            input_dict = {
                "age": [self.age],
                "children": [self.children],
                "bmi": [self.bmi],
                "sex": [self.sex],
                "smoker": [self.smoker],
                "region": [self.region]
            }

            convert_dict = {
                'age': int,
                'children': int,
                'bmi': float,
                'sex': str,
                'smoker': str,
                'region': str
            }

            df = pd.DataFrame(input_dict)

            df = df.astype(convert_dict)
            print(df.info())

            return df

        except Exception as e:
            raise CustomException(e, sys)