import os
import shutil
from pathlib import Path
import yaml
import numpy as np
import pickle
import optuna
from sklearn import linear_model
from sklearn import ensemble
import sklearn.svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
import xgboost as xgb
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score,roc_auc_score

def read_params(config_path: str)-> dict:
    """
                        Method Name: read_params
                        Description: This method performs reading parameters from param.yaml and is a helper
                        function for stage_01_data_preprocessing
                        Output: Return all configuration of yaml to all stages of ML pipeline
                        On Failure: Raise Error

                         Written By: Saurabh Naik
                        Version: 1.0
                        Revisions: None

                        """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)

    return config

def clean_prev_dirs_if_exists(dir_path: str):
    """
                        Method Name: clean_prev_dirs_if_exists
                        Description: This method performs removal of directory if it already exists in order to
                        help stage_01_data_preprocessing.
                        Output: Removes the directory of earlier iteration
                        On Failure: Raise Error

                         Written By: Saurabh Naik
                        Version: 1.0
                        Revisions: None

                        """
    p = Path(__file__).parents[2]
    path = str(p)
    dir_path=os.path.join(path, dir_path)
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)

def create_dir(dirs:list):
    """
                        Method Name: create_dir
                        Description: This method performs creation of directory to help stage_01_data_preprocessing
                        to store preprocessed data into it
                        Output: Creates a directory
                        On Failure: Raise Error

                         Written By: Saurabh Naik
                        Version: 1.0
                        Revisions: None

                        """
    for dir_path in dirs:
        p = Path(__file__).parents[2]
        path = str(p)
        os.makedirs(os.path.join(path, dir_path),exist_ok=True)

def correlation(dataset, threshold):
    """
                        Method Name: correlation
                        Description: This method performs finding correlation among all features of input data
                        and then depending upon the threhold return list of features.
                        Output: Return a list of features having correlation greater than the threshold
                        On Failure: Raise Error

                         Written By: Saurabh Naik
                        Version: 1.0
                        Revisions: None

                        """
    col_corr = set()  # Set of all the names of correlated columns
    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > threshold: # we are interested in absolute coeff value
                colname = corr_matrix.columns[i]  # getting the name of column
                col_corr.add(colname)
    return col_corr


def save_model(model,filename):
        """
                                Method Name: save_model
                                Description: Save the model file to directory
                                Outcome: File gets saved
                                On Failure: Raise Exception

                                Written By: Saurabh Naik
                                Version: 1.0
                                Revisions: None
        """
        model_directory = 'models/'
        try:
            path = os.path.join(model_directory,filename) #create seperate directory for each cluster
            if os.path.isdir(path): #remove previously existing models for each clusters
                shutil.rmtree(model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path) #
            with open(path +'/' + filename+'.pkl',
                      'wb') as f:
                pickle.dump(model, f) # save the model to file

        except Exception as e:
            raise e


def objective(trial,X_train,y_train):
    """
                        Method Name: objective
                        Description: This method is objective function for optuna.
                        Output: returns roc_auc score and accuracy score of best model based on training data
                        On Failure: Raise Exception

                        Written By: Saurabh Naik
                        Version: 1.0
                        Revisions: None

    """
    try:
        classifier_name = trial.suggest_categorical("classifier", ["LogReg", "RandomForest", "SVC", "NaiveBayes",
                                                                   "decision-tree", "xgb"])

        # Step 2. Setup values for the hyperparameters:
        if classifier_name == 'LogReg':
            C = trial.suggest_uniform('C', 0.01, 10)
            classifier_obj = linear_model.LogisticRegression(C=C)

        elif classifier_name == 'RandomForest':
            min_samples_split = trial.suggest_int('min_samples_split', 2, 20)
            min_samples_leaf = trial.suggest_int('min_samples_leaf', 2, 20)
            classifier_obj = sklearn.ensemble.RandomForestClassifier(min_samples_split=min_samples_split,
                                                                     min_samples_leaf=min_samples_leaf)

        elif classifier_name == 'SVC':
            kernel = trial.suggest_categorical('kernel', ['linear', 'poly', 'rbf', 'sigmoid'])
            classifier_obj = sklearn.svm.SVC(kernel=kernel)

        elif classifier_name == 'NaiveBayes':
            var_smoothing = trial.suggest_float("var_smoothing", 1e-4, 0.3, log=True)
            classifier_obj = sklearn.naive_bayes.GaussianNB(var_smoothing=var_smoothing)
        elif classifier_name == 'decision-tree':
            max_depth = trial.suggest_int('max_depth', 5, X_train.shape[1])
            classifier_obj = sklearn.tree.DecisionTreeClassifier(max_depth=max_depth)

        elif classifier_name == 'xgb':
            alpha = trial.suggest_float('alpha', 1e-4, 1)
            subsample = trial.suggest_float('subsample', .1, .5)
            classifier_obj = xgb.XGBClassifier(alpha=alpha, subsample=subsample)

        #Step 3: Scoring method:
        accuracy = []
        roc_auc =[]
        skf = StratifiedKFold(n_splits=10, random_state=None)
        skf.get_n_splits(X_train, y_train)
        # X is the feature set and y is the target
        for train_index, test_index in skf.split(X_train, y_train):
            X1_train, X1_test = X_train.iloc[train_index], X_train.iloc[test_index]
            y1_train, y1_test = y_train.iloc[train_index], y_train.iloc[test_index]

            classifier_obj.fit(X1_train, y1_train)
            prediction = classifier_obj.predict(X1_test)
            score = accuracy_score(prediction, y1_test)
            accuracy.append(score)
            try:
                score1 = roc_auc_score(prediction, y1_test)
                roc_auc.append(score1)
            except ValueError:
                pass
        accuracy=np.array(accuracy).mean()
        roc_auc = np.array(roc_auc).mean()

        return accuracy, roc_auc
    except Exception as e:
        raise e

def find_best_model(X_train,y_train):
    """
                        Method Name: find_best_model
                        Description: This method finds the best model based on accuracy and roc_auc_score.
                        Output: Return the best model hyperparameters
                        On Failure: Raise Exception

                        Written By: Saurabh Naik
                        Version: 1.0
                        Revisions: None

    """
    try:
        sampler = optuna.samplers.NSGAIISampler()
        func = lambda trial: objective(trial, X_train,y_train)
        study = optuna.create_study(directions=["maximize", "maximize"], sampler=sampler)
        study.optimize(func, n_trials=10)
        trial = study.best_trials
        param = trial[0].params
        return param

    except Exception as e:
        raise e

def load_model():
        """
                    Method Name: load_model
                    Description: load the model file to memory
                    Output: The Model file loaded in memory
                    On Failure: Raise Exception

                    Written By: Saurabh Naik
                    Version: 1.0
                    Revisions: None
        """
        path = "C:/Users/Dell/PycharmProjects/Phishing_ml_project/phishing_domain_detection_mlproject/src"
        #path="src"
        #print(os.getcwd())
        model_directory = "/ML_pipelines/models/"
        filename='XGBoost'
        print(str(os.path.normpath(os.getcwd() + os.sep + os.pardir))+"/models/" + filename + '/' + filename + '.sav')
        try:
            # with open(str(os.getcwd())+model_directory + filename + '/' + filename + '.sav',
            #           'rb') as f:
            with open(str(os.path.normpath(os.getcwd() + os.sep + os.pardir))+"/models/" + filename + '/' + filename + '.sav',
                      'rb') as f:
                return pickle.load(f)
        except Exception as e:
            raise e