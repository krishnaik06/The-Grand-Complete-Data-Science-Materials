import os
from sklearn.preprocessing import StandardScaler
from titanic.utils.common import load_object
from titanic.logging import logger
import pandas as pd

class PredictionPipeline:

    def __init__(self, filename):
        self.filename = filename

    def predict(self):
        # loading the model
        model = load_object(os.path.join("artifacts","model_trainer", "model.pkl"))
        logger.info("Model has been loaded successfully")

        # loading the test data
        test_data = self.transform_data()
        logger.info("Test data has been loaded successfully")

        # predicting the test data
        predictions = model.predict(test_data)
        logger.info("Predictions has been made successfully")

        print(predictions)
        return predictions
        # if (predictions==1):
        #     prediction = "Survived"
        #     return [{ "image": prediction}]
        # else:
        #     prediction = "Coccidiosis"
        #     return [{ "image": prediction}]
    
    def transform_data(self):
        # loading the data
        test_data = pd.read_csv(self.filename)
        # logger.info("Test data has been loaded successfully")

        test_data["Sex"] = test_data["Sex"].map({"male": 0, "female": 1})
        
        test_data = test_data.dropna(subset=["Embarked"])

        test_data['Age'] = test_data['Age'].fillna(value=int(test_data['Age'].mean()))

        test_data["Embarked"] = test_data["Embarked"].map({"S": 0, "C": 1, "Q": 2})

        # scaling the dataset
        sdscaler = StandardScaler()
        test_data= sdscaler.fit_transform(test_data)

        return test_data
