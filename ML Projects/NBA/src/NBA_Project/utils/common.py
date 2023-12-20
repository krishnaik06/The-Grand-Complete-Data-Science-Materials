import os
from box.exceptions import BoxValueError
import yaml
from src.NBA_Project import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    

def create_directories(path_to_directories:list, verbose=True):

    """create list of directories
     ARGS:
        path_to_directories: list list of path to directories
        ignore_log (bool,optional): ignore if multiple dirs is to be created
     """
    
    for path in path_to_directories:

        os.makedirs(path, exist_ok=True)

        if verbose:

            logger.info(f"created directory at {path}")

    
@ensure_annotations
def save_json(path:Path,data:dict):

    """save json data

    ARGS:
        path (Path): path to json file
        data (dict): data to saved in json file
        """
    
    with open(path) as f:

        json.dump(data,f,indent=4)

    logger.info(f"json file is created at{path}")

@ensure_annotations
def load_json(path: Path)->ConfigBox:

    with open(path) as f:

        content=json.load()

    logger.info(f"load of json file {path}")

    return ConfigBox(content)

@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")

@ensure_annotations
def load_bin(path:Path)->Any:

    data=joblib.load(path)

    return data

@ensure_annotations
def get_size(path:Path)->str:

    """get sier in KB"""

    size_in_kb=round(os.path.getsize(path)/1024)

    return str(size_in_kb)

