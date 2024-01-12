from src.checkout.constants import CONFIG_FILE_PATH
import yaml
import os
import cv2
import logging
import shutil
from box import ConfigBox

class Datamanipulate:
    '''Manipulation of Image Files'''

    def __init__(self,config_file_path = CONFIG_FILE_PATH):
        self.yaml_path = config_file_path
        with open(config_file_path,'r') as config:
            self.yaml_obj = ConfigBox(yaml.safe_load(config))
    
    def img_converter(self,target_width=640):
        """Specify the target width
        to resize an image"""
        
        modify_yaml_path = self.yaml_obj.model_training.data_manipulate_config
        with open(modify_yaml_path,'r') as config1:
            self.yaml_obj1 = ConfigBox(yaml.safe_load(config1))
            train100_path = self.yaml_obj1.paths.train_path

        for folder in os.listdir(train100_path):
            folder_path = os.path.join(train100_path, folder)
            if os.path.exists(folder_path) and os.path.isdir(folder_path) and os.path.getsize(folder_path)>100:
                train_sub_dir = [os.path.join(folder_path ,subfolder) for subfolder in os.listdir(folder_path) if not subfolder.startswith(('ImageSets','JPEGImages','SegmentationClass','SegmentationObject')) and os.path.isdir(os.path.join(folder_path,subfolder)) and os.path.getsize(os.path.join(folder_path,subfolder))>100]
                for ind_sub_dir in train_sub_dir:
                    for file_name in os.listdir(ind_sub_dir):
                        file_path = (os.path.join(ind_sub_dir,file_name))
                        if os.path.isfile(file_path):
                            image = cv2.imread(str(file_path))
                            if image is not None:
                                original_height, original_width, _ = image.shape
                                target_height = int(
                                    (target_width / original_width) * original_height)

                                if image.shape[1] == target_width and image.shape[0] == target_height:
                                    logging.info(
                                        f"Skipped (already resized): {file_name}  ")
                                    continue

                                resized_image = cv2.resize(
                                    image, (target_width, target_height))
                                cv2.imwrite(str(file_path), resized_image)
                                logging.info(f"Resized: {file_name} ")
                            else:
                                logging.info(f"Failed to read: {file_name} ")
                        else:
                            logging.info(f"{file_name} not a valid file")
