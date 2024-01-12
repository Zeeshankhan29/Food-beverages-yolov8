from src.checkout.components import DataIngestion,DataTransfer, DataTransformation, ModelTraining, DatasetMetaData,Modelevalution,DataAnalytics
from src.checkout.config import Configuration
from src.checkout import logging
import pprint
import sys


def main1():
    config = Configuration()
    data_transfer_config = config.get_data_transfer()
    print(data_transfer_config)
    data_transfer = DataTransfer(data_transfer_config)
    data_transfer.valid_transfer()

def main2():
    config = Configuration()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion = DataIngestion(data_ingestion_config)
    # data_ingestion.resize_img()
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
 


def main4():
    config = Configuration()
    model_training_config = config.get_model_training_config()
    model_training = ModelTraining(model_training_config)
    model_training.yolo_train()

def main5():
    config = Configuration()
    model_evaluation_config = config.get_model_evaluation()
    model_evaluation = Modelevalution(model_evaluation_config)
    model_evaluation.evaluation()

def main6():
    config = Configuration()
    model_analytics_config = config.get_data_analysisconfig()
    model_anlytics = DataAnalytics(model_analytics_config)
    model_anlytics.load_files()
    model_anlytics.analysis()


if __name__ == '__main__':
    try:
        if '--main1' in sys.argv[1:] or 'main1' in sys.argv[1:]:
            main1()
        if '--main2' in sys.argv[1:] or 'main2' in sys.argv[1:]:
            MetaData = main2()
        if '--main3' in sys.argv[1:] or 'main3' in sys.argv[1:]:
            if '--main2' not in sys.argv[1:] and 'main2' not in sys.argv[1:]:
                print("Error: --main3 requires --main2 to be executed first.")
            else:
                main3(MetaData)
        if '--main4' in sys.argv[1:] or 'main4' in sys.argv[1:]:
            main4()
        if '--main5' in sys.argv[1:] or 'main5' in sys.argv[1:]:
            main5()      
        if '--main6' in sys.argv[1:] or 'main6' in sys.argv[1:]:
            main6()      
        
        elif not any(func in sys.argv[1:] for func in ['--main1' ,'--main2','--main3','--main4','--main5','main1','main2','main3','main4','main5']):
            print(f'Function {sys.argv[1:]} defined not valid') 
        
        if len(sys.argv[0:])==1:
            main1()
            MetaData = main2()
            main3(MetaData)
            main4()
            main5() 
            main6()
        
    except Exception as e:
        logging.exception(e)
