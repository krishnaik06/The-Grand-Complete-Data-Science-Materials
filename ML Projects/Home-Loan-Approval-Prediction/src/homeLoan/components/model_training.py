from homeLoan.entity import ModelTrainingConfig
from homeLoan.utils import save_object, evaluate_model
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB


# ModelTraining Component
class ModelTraining:
    def __init__(self, config: ModelTrainingConfig):
        self.config = config

    def initiate_model_training(self, train_arr, test_arr):
        try:
            # Split train, test data
            X_train = train_arr[:,:-1]
            X_test = test_arr[:,:-1]
            y_train = train_arr[:,-1]
            y_test = test_arr[:,-1]

            # List of the Models
            # Here we have classification problem, so we used the list of classification models
            models = {
                'SVC': SVC(),
                'DecisionTreeClassifier': DecisionTreeClassifier(),
                'KNeighborsClassifier': KNeighborsClassifier(),
                'RandomForestClassifier': RandomForestClassifier(),
                'GaussianNB': GaussianNB()
            }

            # Find the best model
            model_report, best_model = evaluate_model(models, X_train, X_test, y_train, y_test)
            print(f'Model Report: {model_report}')
            print(f'Best Model: {best_model}')
            best_model = models[list(best_model.keys())[0]]

            # Save the best model
            save_object(self.config.best_model_path, best_model)

        except Exception as e:
            raise e
