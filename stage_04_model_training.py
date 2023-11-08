
from src.checkout.components import DataIngestion,DataTransformation,ModelTraining
from src.checkout.config import Configuration
from src.checkout import logging



def main4():
    config = Configuration()
    model_training_config = config.get_model_training_config()
    model_training = ModelTraining(model_training_config)
    model_training.yolo_train()


if __name__ =='__main__':
    try:
        main4()
    except Exception as e:
        logging.exception(e)
