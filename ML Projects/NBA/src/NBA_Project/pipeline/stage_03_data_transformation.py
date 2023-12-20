from src.NBA_Project.config.configuration import ConfigurationManager
from src.NBA_Project.components.data_transformation import DataTransformation
from src.NBA_Project import logger
from pathlib import Path


STAGE_NAME="Data Transformation Name"

class DataTransformationTrainingPipeline:

    def __init__(self):

        pass

    def main(self):

        try:

            with open(Path("artifacts/data_validation/status.txt"),"r") as f:
                status=f.read().split(' ')[-1]

            if status=='True':

                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.transform_data()

            else:

                raise Exception("Data is not valid")
            
        except Exception as e:

            print(e)