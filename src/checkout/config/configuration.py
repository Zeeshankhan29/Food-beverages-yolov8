from src.checkout.utils import read_yaml, create_directories
from src.checkout.constants import CONFIG_FILE_PATH
from src.checkout.entity import DataIngestionConfig, DataTransformationConfig, ModelTrainingConfig, DatasetMetaData, DataTransferconfig, Modelevaluationconfig,DataAnalyticsconfig
from box import ConfigBox
from src.checkout import logging
from pathlib import Path


class Configuration:
    def __init__(self, config_file_path=CONFIG_FILE_PATH):
        logging.info(
            f'loading config yaml configuration file: {config_file_path}')
        self.config = read_yaml(config_file_path)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self):
        config = self.config.data_ingestion
        create_directories([config.temp_labels_dir])
        create_directories([config.temp_mask_dir])
        create_directories([config.original_image_dir])

        data_ingestion = DataIngestionConfig(
            temp_dir=config.temp_dir,
            temp_labels_dir=config.temp_labels_dir,
            temp_mask_dir=config.temp_mask_dir,
            original_image_dir=config.original_image_dir,
            yolo_seg_config_file=config.yolo_seg_config_file)
        return data_ingestion

    def get_data_transformation_config(self):
        config = self.config.data_transformation
        create_directories([config.temp_labels_dir])
        create_directories([config.original_image_dir])
        create_directories([config.train_label_dir])
        create_directories([config.test_label_dir])
        create_directories([config.train_image_dir])
        create_directories([config.test_image_dir])
        create_directories([config.yolo_config_dir])
        # logging.info(f'created  directories : {config.temp_labels_dir}, {config.original_image_dir} , {config.train_label_dir} ,{config.test_label_dir} ,{config.train_image_dir},{config.test_image_dir}')

        data_transformation = DataTransformationConfig(temp_labels_dir=config.temp_labels_dir,
                                                       original_image_dir=config.original_image_dir,
                                                       train_label_dir=config.train_label_dir,
                                                       test_label_dir=config.test_label_dir,
                                                       train_image_dir=config.train_image_dir,
                                                       test_image_dir=config.test_image_dir,
                                                       yolo_config_dir=config.yolo_config_dir
                                                       )
        return data_transformation

    def get_model_training_config(self):
        config = self.config.model_training
        create_directories([config.yolo_config_dir])
        model_training = ModelTrainingConfig(yolo_config_dir=config.yolo_config_dir,
                                             yolo_seg_config_file=config.yolo_seg_config_file,
                                            )
        return model_training

    def get_model_metadata_config(self, datasetMetaData):
        datasetMetaData = DatasetMetaData(datasetMetaData=datasetMetaData)
        return datasetMetaData
    
    def get_data_transfer(self):
        config = self.config.data_transfer

        data_transfer_yaml = Path(config.data_transfer_yaml)
       
        data_transfer = DataTransferconfig(class_yaml=data_transfer_yaml)                          
        

        return data_transfer
    
    def get_model_evaluation(self):
        config = self.config.model_evaluation
        model_meta_data = Modelevaluationconfig(modelMetaData=config.train_image_dir)

        return model_meta_data

    def get_data_analysisconfig(self):
        config = self.config.Data_Analytics
        create_directories([config.Analytics_input_dir])
        create_directories([config.Analytics_output_dir])
        data_analytic_dir = DataAnalyticsconfig(Analytics_input_dir=config.Analytics_input_dir,
                                                Analytics_output_dir=config.Analytics_output_dir)

        return data_analytic_dir