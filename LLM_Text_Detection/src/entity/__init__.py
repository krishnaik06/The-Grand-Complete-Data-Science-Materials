# Import necessary modules
from pathlib import Path
from dataclasses import dataclass

# Define a data class for DataIngestion configuration
@dataclass(frozen=True)
class DataIngestionConfig:
    # Path to the directory where data will be stored
    data_dir: Path
    # Path to the file containing text data within the specified data directory
    text_data_file: Path


@dataclass(frozen=True)
class DataTransformationConfig:
    # Path to the directory where cleaned data will be stored
    cleaned_data_dir: Path
    # Path to the file containing cleaned text data within the specified cleaned data directory
    cleaned_text_file: Path
    # Paths to separate text files for training, testing, and validation
    train_text_file: Path
    test_text_file: Path
    valid_text_file: Path


@dataclass
class DataValidationConfig:
    # Path to the directory where validation data will be stored
    validation_dir: Path
    # Path to the file containing validation status information
    status_filepath: Path
    # List of required files for validation
    required_files: list


@dataclass(frozen=True)
class ModelTrainerConfig:
    # Root directory for the model trainer
    root_dir: Path
    # Path to the directory where the trained model will be saved
    trained_model_dir: Path
    # Random seed for reproducibility
    random_seed: int
    # Path to the pre-trained model checkpoint
    model_ckpt: str
    # Number of labels in the classification task
    num_labels: int
    # Learning rate for the optimizer
    learning_rate: float
    # Number of training epochs
    num_train_epochs: int
    # Batch size for training
    train_batch_size: int
    # Number of warm-up steps for the learning rate scheduler
    num_warmup_steps: int
    

@dataclass(frozen=True)
class ModelEvaluationConfig:
    # Root directory for model evaluation
    root_dir: Path
    # evaluation report path
    evaluation_file: Path