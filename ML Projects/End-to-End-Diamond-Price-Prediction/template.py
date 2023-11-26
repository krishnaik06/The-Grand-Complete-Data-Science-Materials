import os
from pathlib import Path

package="DiamondPricePrediction" 

list_of_files = [
    ".github/workflows/main.yaml",
    "Notebook_Experiments/Data/.gitkeep",
    "Notebook_Experiments/Exploratoey_Data_Analysis.ipynb",
    "Notebook_Experiments/Model_Training.ipynb",
    f"src/{package}/__init__.py",
    f"src/{package}/exception.py",
    f"src/{package}/logger.py",
    f"src/{package}/utils/__init__.py",
    f"src/{package}/utils/utils.py",
    f"src/{package}/components/__init__.py",
    f"src/{package}/components/Data_ingestion.py",
    f"src/{package}/components/Data_transformation.py",
    f"src/{package}/components/Model_trainer.py",
    f"src/{package}/pipeline/__init__.py",
    f"src/{package}/pipeline/Prediction_pipeline.py",
    f"src/{package}/pipeline/Training_pipeline.py",
    "static/styles.css",
    "templates/home.html",
    ".gitignore",
    "app.py",
    "Dockerfile",
    "README.md",
    ".dvcignore",
    "dvc.lock",
    "dvc.yaml",
    "requirements.txt",
    "setup.py"]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    if(not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
