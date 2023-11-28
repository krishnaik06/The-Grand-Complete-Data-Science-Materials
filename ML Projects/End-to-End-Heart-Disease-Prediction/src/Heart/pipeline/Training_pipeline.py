from src.Heart.components.Data_ingestion import DataIngestion
from src.Heart.components.Data_transformation import DataTransformation
from src.Heart.components.Model_trainer import ModelTrainer
from src.Heart.components.Model_evaluation import ModelEvaluation


#Data ingestion Pipeline
obj=DataIngestion()
train_data_path,test_data_path=obj.initiate_data_ingestion()

# Data Transformation Pipeline
data_transformation=DataTransformation()
train_arr,test_arr=data_transformation.initialize_data_transformation(train_data_path,test_data_path)

# Model Training Pipeline
model_trainer_obj=ModelTrainer()
model_trainer_obj.initate_model_training(train_arr,test_arr)

# Model Evaluation Pipeline
model_eval_obj = ModelEvaluation()
model_eval_obj.initate_model_evaluation(train_arr,test_arr)