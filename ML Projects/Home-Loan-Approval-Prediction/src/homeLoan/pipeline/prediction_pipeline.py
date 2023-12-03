from homeLoan.utils import read_yaml, load_object
from homeLoan.constants import *


class PredictionPipeline:
    def __init__(self):
        self.config = read_yaml(CONFIG_FILE_PATH)
        self.params = read_yaml(PARAMS_FILE_PATH)
    
    def predict(self, input_features):
        try:
            preprocessor_path = self.config.data_preprocessor.preprocessor_path
            model_path = self.config.model_training.best_model_path

            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)

            # Scale the input features and predict
            scaled_features = preprocessor.transform(input_features)
            prediction = model.predict(scaled_features)
            return prediction[0]

        except Exception as e:
            raise e

         