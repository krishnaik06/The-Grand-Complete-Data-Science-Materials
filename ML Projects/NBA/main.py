from src.NBA_Project import logger
from src.NBA_Project.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from src.NBA_Project.pipeline.stage_02_data_validation import DataValidationPipeline
from src.NBA_Project.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
from src.NBA_Project.pipeline.stage_04_model_trainer import ModelTrainerTrainingPipeline
from src.NBA_Project.pipeline.stage_05_model_evaluation import ModelEvaluationTrainingPipeline
STAGE_NAME="Data ingestion stage"
try:

    logger.info(f">>>>>>>>>>>< stage {STAGE_NAME} stared <<<<<<<<<")

    obj=DataIngestionPipeline()
    obj.main()

    logger.info(f">>>>>>>>>end of {STAGE_NAME}<<<<<<<<<<<<")

except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME="Data Validation stage"
try:

    logger.info(f">>>>>>>>>>>< stage {STAGE_NAME} stared <<<<<<<<<")

    obj=DataValidationPipeline()
    obj.main()

    logger.info(f">>>>>>>>>end of {STAGE_NAME}<<<<<<<<<<<<")

except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME='Data Transformation stage'
try:
    logger.info(f">>>>>>>>> stage {STAGE_NAME} started<<<<<<<<<<<")

    obj=DataTransformationTrainingPipeline()
    obj.main()
    logger.info(f'>>>>><< stage {STAGE_NAME} completed')
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME='Model Trainer Stage'
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = ModelTrainerTrainingPipeline()
    obj.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME='Model Evaluation Stage'
try:
    logger.info(f">>>>>>>>>stage {STAGE_NAME} started <<<<<<<<<")

    model_evaluation=ModelEvaluationTrainingPipeline()
    model_evaluation.main()

    logger.info(f">>>>>>>stage {STAGE_NAME} completed <<<<<<<<<<")

except Exception as e:

    logger.exception(e)

    raise e