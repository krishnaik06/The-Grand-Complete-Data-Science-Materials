from ensure import ensure_annotations
from pathlib import Path
from box import ConfigBox
from box.exceptions import BoxValueError
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import yaml
from titanic.logging import logger
import os
import pickle

@ensure_annotations
def read_yaml(path_to_yaml:Path) -> ConfigBox:
    """
    reads the yaml file and returns the config box for the content of the file

    Agrs:
        path_to_yaml (str) : path like input

    Raises:
        ValuesError: if the yaml file is empty
        e: Empty File

    Returns:
        ConfigBox: ConfigBox type
    """

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f'yaml file {path_to_yaml} loaded successfully')
            return ConfigBox(content)
    
    except BoxValueError:
        raise ValueError('yaml file is empty')
    
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(path_to_dir:list, verbose=True):
    """
    create list of directories

    Args:
        path_to_dir (list): lost of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False

    """
    for path in path_to_dir:
        os.makedirs(path, exist_ok= True)
        if verbose:
            logger.info(f"created directory at: {path}")

@ensure_annotations
def get_size(path:Path) -> str:
    """
    get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
        
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"


@ensure_annotations
def save_object(path:Path, obj):
    """
    save object to file
    """
    try:
        # dir_path = os.path.dirname(path)
        # os.makedirs(dir_path, exist_ok=True)

        with open(path, 'wb') as file:
            pickle.dump(obj, file)
    except Exception as e:
        logger.exception(e)
        raise e

def load_object(path:Path):
    """
    load object from file
    """
    try:
        # dir_path = os.path.dirname(path)

        with open(path, 'rb') as file:
            return pickle.load(file)
        
    except Exception as e:
        logger.exception(e)
        raise e

def evaluate_models(x_train, y_train,x_test, y_test, models, param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            gs = GridSearchCV(model, para, cv=3)
            gs.fit(x_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train) # Training the Model

            y_train_pred = model.predict(x_train)

            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train,y_train_pred)

            test_model_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]]= test_model_score

            return report

    except Exception as e:
        logger.exception(e)
        raise e