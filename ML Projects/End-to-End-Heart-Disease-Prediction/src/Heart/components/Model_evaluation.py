import os
import sys
import mlflow
import pickle
import numpy as np
import mlflow.sklearn
from urllib.parse import urlparse
from src.Heart.utils.utils import load_object
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class ModelEvaluation:
    def __init__(self):
        pass

    def eval_metrics(self,actual,pred):
        accuracy = accuracy_score(actual,pred)
        precision = precision_score(actual,pred)
        recall = recall_score(actual,pred)
        f1 = f1_score(actual,pred)
        return accuracy, precision, recall, f1
    

    def initate_model_evaluation(self, train_array, test_array):
        try:
            X_test,y_test=(test_array[:,:-1], test_array[:,-1])
            model_path=os.path.join("Artifacts","Model.pkl")
            model=load_object(model_path)

            mlflow.set_registry_uri("https://dagshub.com/HemaKalyan45/Heart-Disease-Prediction.mlflow")
                        
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            
            print(tracking_url_type_store)

            with mlflow.start_run():

                predicted_qualities = model.predict(X_test)

                (accuracy, precision, recall, f1) = self.eval_metrics(y_test,predicted_qualities)

                mlflow.log_metric("Testing Accuracy", accuracy)
                mlflow.log_metric("Precision Score", precision)
                mlflow.log_metric("Recall Score", recall)
                mlflow.log_metric("F1 Score", f1)

                # Model registry does not work with file store
                if tracking_url_type_store != "file":

                    # Register the model
                    # There are other ways to use the Model Registry, which depends on the use case,
                    # please refer to the doc for more information:
                    # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                    mlflow.sklearn.log_model(model, "Model", registered_model_name="ml_model")
                else:
                    mlflow.sklearn.log_model(model, "Model")
                
        except Exception as e:
            raise e


