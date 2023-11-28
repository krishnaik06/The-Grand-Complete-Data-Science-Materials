from Indian_Coin_Detection import logger
from Indian_Coin_Detection.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from Indian_Coin_Detection.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from Indian_Coin_Detection.pipeline.stage_03_training import ModelTrainingPipeline


STAGE_NAME = "Data Ingestion stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e


STAGE_NAME = "Data Validation stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   obj = DataValidationTrainingPipeline()
   validation_status = obj.main()
   logger.info(f"Successfully completed Data Validation with validation status {validation_status}")
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
   logger.exception(e)
   raise e

STAGE_NAME = "Training"
try: 
   logger.info(f"*******************")
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   if validation_status:
      model_trainer = ModelTrainingPipeline()
      model_trainer.main()
      logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
   else:
       logger.info("Data Validation Stauts is False.")
except Exception as e:
        logger.exception(e)
        raise e

