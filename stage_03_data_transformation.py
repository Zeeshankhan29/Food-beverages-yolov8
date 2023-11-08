from src.checkout.components import DataIngestion,DataTransformation,ModelTraining
from src.checkout.config import Configuration
from src.checkout import logging


def main2():
    config = Configuration()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion = DataIngestion(data_ingestion_config)
    data_ingestion.resize_img()
    data_ingestion.data_valid()
    data_ingestion.data_counter()
    return data_ingestion.yolo_polygon_to_label1()
  


def main3(datasetMetaData: list):
    config = Configuration()
    data_transformation_config = config.get_data_transformation_config()
    Meta_data = config.get_model_metadata_config(datasetMetaData)
    data_transformation = DataTransformation(data_transformation_config, Meta_data)
    data_transformation.split_train_test()
    data_transformation.instance_validataion()
    data_transformation.data_validation()
    data_transformation.metadata_generator()



if __name__ =='__main__':
    try:
        datasetMetaData =  main2()
        main3(datasetMetaData)
    except Exception as e:
        logging.exception(e)