from src.checkout.components import Modelevalution
from src.checkout.config import Configuration
from src.checkout import logging
import pprint

def main5():
    config = Configuration()
    model_evaluation_config = config.get_model_evaluation()
    model_evaluation = Modelevalution(model_evaluation_config)
    model_evaluation.evaluation()
    

if __name__ == '__main__':
    try:
        
        main5()
 
    except Exception as e:
        logging.exception(e)