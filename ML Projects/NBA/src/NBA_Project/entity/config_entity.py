from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:

    root_dir: Path
    source: Path
    local_data_file:Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir:Path
    STATUS_FILE:str
    unzip_data_dir:Path
    all_schema:dict


@dataclass(frozen=True)
class DataTransformationConfig:

    root_dir: Path
    data_path: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    columns: dict
    model_name: str
    C: float
    class_weight: str
    penalty: str
    solver: str
    target_column: str


@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    all_params: dict
    all_columns: dict
    metric_file_name: Path
    target_column: str