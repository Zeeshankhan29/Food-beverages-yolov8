from src.checkout.components import DataTransfer
from src.checkout.config import Configuration
from src.checkout import logging
import pprint


def main1():
    config = Configuration()
    data_transfer_config = config.get_data_transfer()
    print(data_transfer_config)
    data_transfer = DataTransfer(data_transfer_config)
    data_transfer.valid_transfer()



if __name__ == "__main__":
    try:
        main1()
    except Exception as e:
        logging.exception(e)