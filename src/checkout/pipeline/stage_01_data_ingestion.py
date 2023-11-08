from src.checkout.config import Configuration
from src.checkout.components import DataIngestion
from src.checkout import logger


def main():
    config = Configuration()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion = DataIngestion(data_ingestion_config)
    # data_ingestion.download_data()
    # data_ingestion.split_data()
    data_ingestion.yolo_polygon_to_label1()

if __name__ =='__main__':
    try:
        main()
    except Exception as e:
        logger.exception(e)