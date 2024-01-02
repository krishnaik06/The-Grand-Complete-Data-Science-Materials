import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = 'homeLoan'

list_of_files = [
    # For github action
    '.github/workflows/.gitkeep', 
    f'src/{project_name}/__init__.py',

    # For Logger
    f'src/{project_name}/logger/__init__.py',

    # For Components
    f'src/{project_name}/components/__init__.py',
    f'src/{project_name}/components/data_ingestion.py',
    f'src/{project_name}/components/data_preprocessing.py',
    f'src/{project_name}/components/model_training.py',

    # For Utils
    f'src/{project_name}/utils/__init__.py',
    f'src/{project_name}/utils/common.py',

    # For Config
    f'src/{project_name}/config/__init__.py',
    f'src/{project_name}/config/configuration.py',

    # For Pipeline
    f'src/{project_name}/pipeline/__init__.py',
    f'src/{project_name}/pipeline/training_pipeline.py',
    f'src/{project_name}/pipeline/prediction_pipeline.py',

    # For Entity
    f'src/{project_name}/entity/__init__.py',
    f'src/{project_name}/entity/config_entity.py',

    # For Constants
    f'src/{project_name}/constants/__init__.py',

    # For Notebooks
    'notebooks/exploratory_data_analysis.ipynb',
    'notebooks/data_ingestion.ipynb',
    'notebooks/data_preprocessing.ipynb',
    'notebooks/model_training.ipynb',

    # For Config & Params
    'config/config.yaml',
    'params.yaml',

    # For Local Package
    'setup.py',

    # Required Packages
    'requirements.txt'
]


for filepath in list_of_files:
    
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    print(filedir + "--" + filename)

    if (filedir != '') and (not os.path.exists(filedir)):
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            logging.info(f"Creating empty file: {filename}")

    else:
        logging.info(f"{filename} already exists")

    
    
    