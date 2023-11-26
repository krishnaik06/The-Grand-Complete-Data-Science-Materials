from src.DiamondPricePrediction.components.Data_ingestion import DataIngestion

from src.DiamondPricePrediction.components.Data_transformation import DataTransformation

from src.DiamondPricePrediction.components.Model_trainer import ModelTrainer

from src.DiamondPricePrediction.components.Model_evaluation import ModelEvaluation



obj=DataIngestion()
train_data_path,test_data_path=obj.initiate_data_ingestion()

data_transformation=DataTransformation()
train_arr,test_arr=data_transformation.initialize_data_transformation(train_data_path,test_data_path)

model_trainer_obj=ModelTrainer()
model_trainer_obj.initate_model_training(train_arr,test_arr)

model_eval_obj = ModelEvaluation()
model_eval_obj.initiate_model_evaluation(train_arr,test_arr)