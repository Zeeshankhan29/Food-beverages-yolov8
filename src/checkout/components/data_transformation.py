from src.checkout.entity import DataTransformationConfig, DatasetMetaData
from src.checkout.utils import read_yaml
import os
import sys
from pathlib import Path
from ultralytics import YOLO
import os
import cv2
import shutil
from src.checkout import logging
import re
from box import ConfigBox
import math
import yaml
import pandas as pd
import time


class DataTransformation:
    def __init__(self, DataTransformation=DataTransformationConfig, datasetMetaData=DatasetMetaData):
        self.transformation = DataTransformation
        self.MetaData = datasetMetaData
        self.curr_dir = Path(os.getcwd())
        self.input_dir = Path(self.transformation.temp_labels_dir)
        self.output_dir = Path(self.transformation.original_image_dir)
        self.train_label_dir = Path(self.transformation.train_label_dir)
        self.test_label_dir = Path(self.transformation.test_label_dir)
        self.train_image_dir = Path(self.transformation.train_image_dir)
        self.test_image_dir = Path(self.transformation.test_image_dir)
        self.params_path = os.path.join(self.curr_dir, 'params.yaml')
        self.yoloconfig = read_yaml(Path(os.path.join(self.transformation.yolo_config_dir,'task-seg.yaml')))

    def split_train_test(self):
        yaml_split = {}
        if os.path.exists(self.params_path):
            with open(self.params_path, 'r') as params_file:
                yaml_split = yaml.safe_load(params_file) or {}

        default_split  = {'split_point': 0.8}
        merged_split = {**default_split,**yaml_split}

        ##value from params yaml file
        split = ConfigBox(merged_split)


        dmd = self.MetaData.datasetMetaData
        for dict in dmd:
            obj = ConfigBox(dict)
            print(
                f'Class name = {obj.classname}, Class index = {obj.classindex}\n Mask Files Length = {obj.mask_files_len},  Original Files Length = {obj.original_files_len},  Mask Files Length = {obj.mask_files_len},  Label Files Length = {obj.label_files_len} \n')
            if obj.label_files_len > 199:
                if obj.label_files_len == obj.original_files_len:
                    # Calculate the split point for an odd-length split
                    split_point = int(math.ceil(obj.label_files_len * split.split_point))
                    for index, ignorefile in enumerate(obj.original_files):
                        if index <= split_point:
                            shutil.copy(
                                obj.original_files[index], self.train_image_dir)
                            shutil.copy(
                                obj.label_files[index], self.train_label_dir)
                        if index > split_point:
                            shutil.copy(
                                obj.original_files[index], self.test_image_dir)
                            shutil.copy(
                                obj.label_files[index], self.test_label_dir)
    
    def instance_validataion(self):
        meta = self.MetaData.datasetMetaData
        logging.info('\n')
        logging.info(f'{"*"*20}Instances Calculation Started{"*"*20}')
        meta_value = {}
        for data in meta:
            obj = ConfigBox(data)
            label_file = obj.label_files
            label_name = obj.classname
            
           
            for index , txt_file in enumerate(label_file):
                with open(label_file[index],'r') as f:
                    value = len(f.readlines())
                    
                    if label_name in meta_value:
                        meta_value[label_name] += value
                        
                    else:
                        meta_value[label_name] = value
            logging.info(f'Instance calculation started  for ---> {label_name}')
        logging.info(f'{"*"*20}Instance calculation finished {20*"*"}')
        
        for folder, instance in meta_value.items():
                logging.info(f"{folder} has --> {instance} Instances")
      


    def data_validation(self):
        train_img_path = os.path.join(self.curr_dir, self.train_image_dir)
        test_img_path = os.path.join(self.curr_dir, self.test_image_dir)
        train_label_path = os.path.join(self.curr_dir, self.train_label_dir)
        test_label_path = os.path.join(self.curr_dir, self.test_label_dir)

        img_train_files = len(os.listdir(train_img_path))
        img_val_files = len(os.listdir(test_img_path))
        label_train_files = len(os.listdir(train_label_path))
        label_val_files = len(os.listdir(test_label_path))

        if img_train_files != label_train_files or img_val_files != label_val_files:
            logging.info(
                '\n**********************************************************************************')
            logging.info(
                f"Image train folder has {img_train_files} files and Label train folder has {label_train_files} labels")
            logging.info(
                f"Image val folder has {img_val_files} files and Label val folder has {label_val_files} labels")
            logging.info('Mismatch data between labels and images')
            logging.info('Critical error stopped Execution')
            exit(0)
        else:
            logging.info(
                '\n**********************************************************************************')
            logging.info(
                f"Image train folder has {img_train_files} files and Label train folder has {label_train_files} labels")
            logging.info(
                f"Image val folder has {img_val_files} files and Label val folder has {label_val_files} labels")
            logging.info('Test cases passed')
            logging.info('Model is ready to Train')


    def metadata_generator(self):
        meta_data =[ ]

        for folder in sorted(os.listdir(self.output_dir)):
            ob = self.yoloconfig
            names = ob.names
            if folder in names:
                # Original files metadata
                org_file_dir = [os.path.join(self.curr_dir,self.output_dir,folder,filename) for filename in os.listdir(os.path.join(self.curr_dir,self.output_dir,folder))]
                
                #Label files metadata
                label_file_dir = [os.path.join(self.curr_dir,self.input_dir,folder,filename) for filename in os.listdir(os.path.join(self.curr_dir,self.input_dir,folder))]

                #Generate csv file 
                meta_data.append({
                "classname": folder,
                "original_files":org_file_dir,
                "label_files":label_file_dir,
                
                
                })

        df = pd.DataFrame(meta_data)
        os.makedirs('metadata',exist_ok=True)
        df.to_csv(f'metadata/Metadata{time.time()}.csv',index=False)