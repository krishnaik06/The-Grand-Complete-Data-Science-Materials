import os
from pathlib import Path
from sklearn.metrics import accuracy_score
from titanic.entity import ModelTrainerConfig
from titanic.logging import logger
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
# from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.preprocessing import StandardScaler
# from sklearn.tree import train_test_split

from sklearn.model_selection import train_test_split

from titanic.utils.common import save_object

class ModelTrainer:
    def __init__(self, config:ModelTrainerConfig):
        self.config = config

    def fetch_transformed_data(self):
        df = pd.read_csv(self.config.data_path)
        logger.info("Data has been fetched successfully")
        return df
    
    def scaling_data(self):
        df = self.fetch_transformed_data()

        x = df.drop(columns='Survived', axis=1)
        y = df['Survived']

        sd = StandardScaler()
        x = sd.fit_transform(x)


        logger.info("Data has been scaled successfully")
        return x,y

    def initiate_model_training(self):
        x, y = self.scaling_data()

        models = {
                "Random Forest": RandomForestClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "K-Neighbors Regressor": KNeighborsClassifier(),
                "CatBoosting Regressor": CatBoostClassifier(verbose=False),
                "AdaBoost Regressor": AdaBoostClassifier()
                # "XGBRegressor": XGBClassifier(),
                # "Linear Regression": LinearRegression(),
            }
        # For Hyper Parameter tuning 
        # model_report:dict = evaluate_models(x_train = x_train, y_train = y_train,x_test=x_test, y_test=y_test, models=models, param = params)
        accuracy_dict = {}
        for model_name, model in models.items():
            model.fit(x, y)
            logger.info(f"Model {model_name} has been trained successfully")
            y_pred = model.predict(x)
            accuracy = accuracy_score(y, y_pred)
            accuracy_dict[accuracy] = (model, model_name, accuracy)
        
        
        # best_model = list(models.values())[accuracy_list.index(max(accuracy_list))]
        # best_model = max(list(accuracy_dict.values()))
        best_model = accuracy_dict[max(accuracy_dict)][0]
        
        model_path= Path(os.path.join(self.config.root_dir,"model.pkl"))

        save_object(path = model_path,obj =best_model)
        logger.info(f"Model Name: {accuracy_dict[max(accuracy_dict)][1]} has been saved successfully with accuracy: {accuracy_dict[max(accuracy_dict)][2]}")

        logger.info("Model Training Complete")