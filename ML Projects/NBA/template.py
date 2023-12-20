import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s:')


project_name='NBA_Project'

list_of_files=[
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    'schema.yaml',
    'main.py',
    'app.py',
    'requirements.txt',
    'setup.py',
    'research/trials.ipynb',
    'templates/index.html'
]

for filepath in list_of_files:


    filepath=Path(filepath) #transform to windows path
    folder_name,file_name=os.path.split(filepath)

    if folder_name!="":

        os.makedirs(folder_name,exist_ok=True)

        logging.info(f"creating; {folder_name} for file {file_name}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):

        with open(filepath,"w") as f:

            pass
            logging.info(f"creating empty file: {filepath}")

    else:
        logging.info(f"{folder_name} is already exists")



