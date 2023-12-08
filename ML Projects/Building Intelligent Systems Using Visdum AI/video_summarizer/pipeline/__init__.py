from video_summarizer.components.data_ingestion import DataIngestion
from video_summarizer.components.data_validation import DataValidation
from video_summarizer.components.data_preprocessing import DataProcessingConfig
from video_summarizer.components.data_preprocessing import DataProcessing
from video_summarizer.components.model_trainer import ModelTrainer
import os, sys
from dataclasses import dataclass

@dataclass
class TrainingPipelineConfig:
    artifacts_folder = "artifacts"
    data_ingestion_artifacts = os.path.join(artifacts_folder, "data_ingestion")
    data_processing_artifacts = os.path.join(artifacts_folder, "data_processing")
    model_trainer_artifacts = os.path.join(artifacts_folder, "model_trainer")

def create_directories(config=TrainingPipelineConfig):
    # Check if the artifacts folder exists
    if not os.path.exists(config.artifacts_folder):
        os.makedirs(config.artifacts_folder)

    # Check and create the data ingestion artifacts folder
    if not os.path.exists(config.data_ingestion_artifacts):
        os.makedirs(config.data_ingestion_artifacts)

    # Check and create the data processing artifacts folder
    if not os.path.exists(config.data_processing_artifacts):
        os.makedirs(config.data_processing_artifacts)

    # Check and create the model trainer artifacts folder
    if not os.path.exists(config.model_trainer_artifacts):
        os.makedirs(config.model_trainer_artifacts)
    
def run_training_pipeline(config=TrainingPipelineConfig):
    # Create Directories
    create_directories()
    # create an instance of the `DataIngestion` class and assign variable as `downloader`.
    downloader = DataIngestion(dataset_name="lighteval/summarization", subset="xsum", save_folder=config.data_ingestion_artifacts)
    downloader.download_dataset()
    # create an instance of the `DataValidation` class and assign variable as `validator`.
    validator = DataValidation(dataset_folder=config.data_ingestion_artifacts)
    validator.check_dataset()

    # create an instance of the config dataclass for data processing component
    data_processing_config = DataProcessingConfig(max_input_length=128, max_target_length=64, dataset_folder=config.data_ingestion_artifacts, artifacts_folder=config.data_processing_artifacts)
    # create an instance of the 'DataProcessing' class and assigns variable as 'processor'.
    processor = DataProcessing(data_processing_config)
    processor.process_data()

    # create an instance of the `ModelTrainer` class with the specified parameters.
    trainer = ModelTrainer(model_checkpoint='facebook/bart-base', 
                           processed_dataset_folder=config.data_processing_artifacts, 
                           trainer_artifact_dir=config.model_trainer_artifacts)
    trainer.train()