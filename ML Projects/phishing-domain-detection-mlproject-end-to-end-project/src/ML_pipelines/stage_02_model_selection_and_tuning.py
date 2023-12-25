import argparse
from src.application_logging.logger import App_Logger
from src.utils.common_utils import read_params, save_model,find_best_model
import pandas as pd
from pathlib import Path
from sklearn import linear_model
from sklearn import ensemble
import sklearn.svm
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score,roc_auc_score

def model_selection_and_tuning(config_path):
    """
                    Method Name: model_selection_and_tuning
                    Description: Selects a best model from all classification model having best accuracy and auc_roc_score
                    and does hyperparameter tuning
                    Output: Best model selected for each cluster
                    On Failure: Raise Exception

                     Written By: Saurabh Naik
                    Version: 1.0
                    Revisions: None

                    """
    try:
        # Initializing Logger object
        logger = App_Logger()
        p = Path(__file__).parents[2]
        path = str(p) + "/src/Training_Logs/ModelSelectionAndTuningLog.txt"
        file = open(path, "a+")
        logger.log(file, "Model Selection and tuning process Started ")

        # Reading of params from params.yaml file
        config = read_params(config_path)
        target_col = config["base"]["target_col"]
        train_data_path = config["preprocessed_data"]["train_data"]
        test_data_path = config["preprocessed_data"]["test_data"]

        # Reading test and train clustered data
        p = Path(__file__).parents[2]
        train_path = str(p) + str(train_data_path)
        logger.log(file, 'Reading training data')
        clustered_train_data = pd.read_csv(train_path)
        test_path = str(p) + str(test_data_path)
        logger.log(file, 'Reading test data')
        clustered_test_data = pd.read_csv(test_path)
        logger.log(file, 'Reading of train and test data done successfully!! Now model selection begins')

        #Model Selection
        X_train1 = clustered_train_data.drop(labels=target_col, axis=1)
        X_test1 = clustered_test_data.drop(labels=target_col, axis=1)
        y_train1 = clustered_train_data[[target_col]]
        y_test1 = clustered_test_data[[target_col]]
        param = find_best_model(X_train1, y_train1)
        logger.log(file, 'Hyperparameter tuning is completed and after comparing auc_roc_score '
                                 'and accuracy score of models we going to select model having hyperparameters: ' + str(param))
        args1={key: val for key,
            val in param.items() if key != 'classifier'}
        if param['classifier']=='LogReg':
            classifier_obj = linear_model.LogisticRegression(**args1)
            model_name='LogisticRegression'
        elif param['classifier']=='RandomForest':
            classifier_obj = sklearn.ensemble.RandomForestClassifier(**args1)
            model_name = 'RandomForest'
        elif param['classifier']=='SVC':
            classifier_obj = sklearn.svm.SVC(**args1)
            model_name = 'SVC'
        elif param['classifier']=='NaiveBayes':
            classifier_obj = sklearn.naive_bayes.GaussianNB(**args1)
            model_name = 'NaiveBayes'
        elif param['classifier']=='decision-tree':
            classifier_obj = sklearn.tree.DecisionTreeClassifier(**args1)
            model_name = 'DecisionTree'
        elif param['classifier']=='xgb':
            classifier_obj = xgb.XGBClassifier(**args1)
            model_name = 'XGBoost'
        classifier_obj.fit(X_train1,y_train1)
        logger.log(file, 'model trained Successfully!! Now testing begins')
        y_pred = classifier_obj.predict(X_test1)
        logger.log(file, 'confusion_matrix ' + str(confusion_matrix(y_test1, y_pred)))
        logger.log(file, 'accuracy_score ' + str(accuracy_score(y_test1, y_pred)))
        logger.log(file, 'roc_auc_score ' + str(roc_auc_score(y_test1, y_pred)))
        logger.log(file, 'classification_report ' + str(classification_report(y_test1, y_pred)))
        logger.log(file,'model tested successfully!!')

        logger.log(file, 'Starting to Save ML model')
        save_model(classifier_obj, model_name)
        logger.log(file, model_name+'Model Saved')
        logger.log(file, 'Model Selection and tuning Completed')



    except Exception as e:
        logger = App_Logger()
        p = Path(__file__).parents[2]
        path = str(p) + "/src/Training_Logs/ModelSelectionAndTuningLog.txt"
        file = open(path, "a+")
        logger.log(file, "error encountered due to: %s" % e)
        raise e


if __name__ == '__main__':
    p = Path(__file__).parents[2]
    path=str(p) + "\params.yaml"
    args = argparse.ArgumentParser()
    args.add_argument("--config", default=path)
    parsed_args = args.parse_args()

    try:

        data = model_selection_and_tuning(config_path=parsed_args.config)
    except Exception as e:
        raise e