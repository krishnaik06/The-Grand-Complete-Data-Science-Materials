from sklearn.metrics import precision_score, recall_score, f1_score
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from src.NBA_Project.entity.config_entity import ModelEvaluationConfig
from src.NBA_Project.utils.common import save_json

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config


    def eval_metrics(self,actual,pred):

        precision=precision_score(actual,pred)
        recall=recall_score(actual,pred)
        f1=f1_score(actual,pred)

        return precision,recall,f1
    
    def save_results(self):

        schema=self.config.all_columns

        column_list = list(schema.keys())


        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.target_column], axis=1)
        test_x = test_x[column_list]
        print(test_x.columns)
        test_y = test_data[[self.config.target_column]]

        predicted_perf = model.predict(test_x)
        (precision,recall,f1)=self.eval_metrics(test_y, predicted_perf)
        scores = {"Precision": precision, "Recall": recall, "f1_score": f1}


        save_json(path=Path(self.config.metric_file_name), data=scores)

