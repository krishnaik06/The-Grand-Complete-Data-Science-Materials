from titanic.components.data_transformation import DataTransformation
from titanic.config.configuration import ConfigurationManager
from titanic.logging import logger

class DataTransformationTrainingPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        data_tranformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(data_tranformation_config)
        data_transformation.save_transformed_data()

if __name__ == __name__:
    STAGE_NAME = 'Data Transformation Stage'

    try:
        logger.info(f">>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
        data_transformation = DataTransformationTrainingPipeline()
        data_transformation.main()
        logger.info(f">>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<< \n\n x=========================x \n\n")

    except Exception as e:
        logger.exception(e)
        raise e