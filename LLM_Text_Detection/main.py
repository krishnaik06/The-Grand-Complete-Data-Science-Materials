# Import necessary modules and classes
import sys
from src.pipeline.data_ingestion_pipeline import DataIngestionTraining
from src.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.pipeline.data_validation_pipeline import DataValidator
from src.pipeline.model_training_pipeline import ModelTrainerPipeline
from src.pipeline.model_evaluation_pipeline import ModelEvaluationPipeline
from src.logger import logging
from src.exception import CustomException


# Define a constant for the stage name
STAGE_NAME = "Data Ingestion"
# Data Ingestion Stage
try:
    logging.info(f"--------------------{STAGE_NAME} start--------------------")
    print(f"--------------------{STAGE_NAME} start--------------------")
    # Instantiate the DataIngestionTraining class
    obj = DataIngestionTraining()
    # Execute the main method to perform data ingestion
    ingest_data_path = obj.main()
    logging.info(f"------------------------{STAGE_NAME} end--------------------")
    print(f"------------------------{STAGE_NAME} end--------------------")
except Exception as e:
    # Log and raise an exception if an error occurs during data ingestion
    logging.error(f"Error in {STAGE_NAME}: {str(e)}")
    print(f"Error in {STAGE_NAME}: {str(e)}")
    raise CustomException(e, sys)

# Data Transformation Stage
STAGE_NAME = "Data Transformation"
try:
    logging.info(f"--------------------{STAGE_NAME} start--------------------")
    print(f"--------------------{STAGE_NAME} start--------------------")
    # Instantiate the DataTransformationPipeline class with the path to the ingested data
    obj = DataTransformationPipeline(ingest_data_path)
    # Execute the main method to perform data transformation
    cleaned_text_path = obj.main()
    logging.info(f"------------------------{STAGE_NAME} end--------------------")
    print(f"------------------------{STAGE_NAME} end--------------------")
except Exception as e:
    # Log and raise an exception if an error occurs during data transformation
    logging.error(f"Error in {STAGE_NAME}: {str(e)}")
    f"Error in {STAGE_NAME}: {str(e)}"
    raise CustomException(e, sys)

# Data Validation Stage
STAGE_NAME = "Data Validation"
try:
    logging.info(f"--------------------{STAGE_NAME} start--------------------")
    print(f"--------------------{STAGE_NAME} start--------------------")
    # Instantiate the DataValidator class with the path to the cleaned text data
    obj = DataValidator(cleaned_text_path)
    # Execute the main method to perform data validation
    obj.main()
    logging.info(f"------------------------{STAGE_NAME} end--------------------")
    print(f"------------------------{STAGE_NAME} end--------------------")
except Exception as e:
    # Log and raise an exception if an error occurs during data validation
    logging.error(f"Error in {STAGE_NAME}: {str(e)}")
    f"Error in {STAGE_NAME}: {str(e)}"
    raise CustomException(e, sys)

# Model Training Stage
STAGE_NAME = "Model Trainer"
try:
    logging.info(f"--------------------{STAGE_NAME} start--------------------")
    print(f"--------------------{STAGE_NAME} start--------------------")
    # Instantiate the ModelTrainerPipeline class with the paths to the cleaned text data
    obj = ModelTrainerPipeline(cleaned_text_path[0], cleaned_text_path[1])
    # Execute the main method to perform model training
    evaluation_data, trained_model_path = obj.main()
    logging.info(f"------------------------{STAGE_NAME} end--------------------")
    print(f"------------------------{STAGE_NAME} end--------------------")
except Exception as e:
    # Log and raise an exception if an error occurs during model training
    logging.error(f"Error in {STAGE_NAME}: {str(e)}")
    f"Error in {STAGE_NAME}: {str(e)}"
    raise CustomException(e, sys)

# Model Evaluation stage
STAGE_NAME = "Model Evaluation"
try:
    logging.info(f"--------------------{STAGE_NAME} start--------------------")
    print(f"--------------------{STAGE_NAME} start--------------------")
    # Instantiate the ModelEvaluationPipeline class
    obj = ModelEvaluationPipeline(evaluation_data, trained_model_path)
    # Execute the main method to perform model training
    obj.main()
    logging.info(f"------------------------{STAGE_NAME} end--------------------")
    print(f"------------------------{STAGE_NAME} end--------------------")
except Exception as e:
    # Log and raise an exception if an error occurs during model training
    logging.error(f"Error in {STAGE_NAME}: {str(e)}")
    f"Error in {STAGE_NAME}: {str(e)}"
    raise CustomException(e, sys)
