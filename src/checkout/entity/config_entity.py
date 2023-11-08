from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataTransferconfig:
    class_yaml : Path


@dataclass(frozen=True)
class DataIngestionConfig:
    temp_dir : Path
    temp_labels_dir : Path
    temp_mask_dir : Path
    original_image_dir : Path
    yolo_seg_config_file: Path


@dataclass(frozen=True)
class DataTransformationConfig:
    temp_labels_dir :Path
    original_image_dir :Path
    train_label_dir :Path
    test_label_dir:Path
    train_image_dir : Path
    test_image_dir : Path
    yolo_config_dir: Path


@dataclass(frozen=True)
class ModelTrainingConfig:
    yolo_config_dir: Path
    yolo_seg_config_file: str
   

@dataclass(frozen=True)
class DatasetMetaData:
    datasetMetaData : list


@dataclass(frozen=True)
class Modelevaluationconfig:
    modelMetaData : Path