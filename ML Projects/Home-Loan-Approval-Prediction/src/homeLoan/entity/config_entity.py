# Config Entity
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    source_url: str
    raw_dataset_dir: Path
    raw_data_path: str
    train_data_path: Path
    test_data_path: Path

@dataclass(frozen=True)
class DataPreprocessingConfig:
    train_data_path: Path
    test_data_path: Path
    preprocessor_path: Path

@dataclass(frozen=True)
class ModelTrainingConfig:
    best_model_path: Path
    