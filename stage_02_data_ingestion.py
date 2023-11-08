from src.checkout.config import Configuration
from src.checkout.components import DataIngestion
from src.checkout import logging


def main2():
    config = Configuration()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion = DataIngestion(data_ingestion_config)
    data_ingestion.resize_img()
    data_ingestion.data_valid()
    data_ingestion.data_counter()
    return data_ingestion.yolo_polygon_to_label1()

if __name__ =='__main__':
    try:
        datasetMetaData =  main2()
    except Exception as e:
        logging.exception(e)