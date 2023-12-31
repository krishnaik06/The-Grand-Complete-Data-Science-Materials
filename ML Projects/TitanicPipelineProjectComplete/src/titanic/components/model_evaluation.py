import os
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from titanic.entity import ModelEvaluationConfig
from titanic.utils.common import load_object
from sklearn.metrics import accuracy_score, confusion_matrix
from titanic.logging import logger
import pandas as pd
import yaml

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def load_dataset(self):
        df = pd.read_csv(self.config.data_path)
        logger.info("Data loaded successfully for model evaluation")
        return df
    
    def scaled_data(self):
        df = self.load_dataset()

        x = df.drop(columns='Survived', axis=1)
        y = df['Survived']

        sd = StandardScaler()
        x = sd.fit_transform(x)


        logger.info("Data has been scaled successfully")
        return x,y

    def evaluate(self):

        x,y_true = self.scaled_data()

        model = load_object(Path(os.path.join("artifacts","model_trainer","model.pkl")))
        logger.info("Model Loaded successfully for model evaluation")

        y_pred = model.predict(x)

        accuracy = accuracy_score(y_true=y_true, y_pred=y_pred)
        cm = confusion_matrix(y_true=y_true, y_pred=y_pred)

        logger.info(f"Accuracy of the Model: {accuracy}")
        logger.info(f"Confusion Matrix of the Model: {cm}")

        content = dict()
        content['accuracy'] = str(accuracy)
        content['confusion_matrix'] = str(cm)

        return content
    
    def save_metrics(self):
        content = self.evaluate()
        logger.info(f"Metrics saved to {self.config.metrics_file_name}")

        with open(self.config.metrics_file_name, 'w') as f:
            yaml.dump(content, f)
        