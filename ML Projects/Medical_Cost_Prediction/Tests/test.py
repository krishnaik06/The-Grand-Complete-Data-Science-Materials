import sys
import os
import pandas as pd
from src.exception import CustomException
from src.utils import load_object
from sklearn.metrics import r2_score

class Testing:
    def __init__(self):
        pass

    def get_test_results(self, test_df):
        try:
            model_path = os.path.join("artifacts","model.pkl")
            preprocessor_path = os.path.join("artifacts","preprocessor.pkl")

            model = load_object(file_path = model_path)
            print("Best Model:{}".format(model))

            preprocessor = load_object(file_path = preprocessor_path)

            target_column_name = 'charges'
            features = test_df.drop(columns=[target_column_name], axis=1)
            target = test_df[target_column_name]

            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            r2 = r2_score(target, preds)
            return r2
        
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__=='__main__':
    testing = Testing()

    test_df = pd.read_csv('artifacts/test.csv')
    r2_ = testing.get_test_results(test_df)

    print("Test R2 Score: {}".format(round(r2_,2)))

