from src.checkout.entity import DataTransferconfig
from src.checkout.utils import read_yaml
import time
import os
from box import ConfigBox
from pathlib import Path
import shutil
from src.checkout import logging


class DataTransfer:
    def __init__(self,DataTransferConfig=DataTransferconfig):
        self.transfer = DataTransferConfig
        self.transfer = read_yaml(self.transfer.class_yaml)


    def valid_transfer(self):
        start = time.time()

        os.makedirs('artifacts/temp/mask',exist_ok=True)
        os.makedirs('artifacts/temp/original',exist_ok=True)

        #original data
        original_data = tuple(sorted(self.transfer.original_data))

        #mask data
        mask_data = tuple(sorted(self.transfer.mask_data))

        # Include files defined
        meta_files = set(self.transfer.meta_class)

        # exclude files defined
        exclude_files = set(self.transfer.exclude_class)

        valid_objects = sorted(tuple(meta_files.difference(exclude_files)))
        logging.info(f'{"*"*20}Data Transfer stage started{"*"*20}')


       
        meta_data ={}
        img=[]
        label=[]
        for file in valid_objects:
            for file1 in sorted(os.listdir(os.path.join(self.transfer.training_path,file))):
                if file1.startswith(original_data):
                    image_path = os.listdir(os.path.join(self.transfer.training_path,file,file1))
                    image_path = sorted(image_path)
                    for index , file_name in enumerate(image_path):
                        img.append(os.path.join(self.transfer.training_path,file,file1,image_path[index]))
                        
                elif file1.startswith(mask_data):
                    label_path = sorted(os.listdir(os.path.join(self.transfer.training_path,file,file1)))
                    label_path = sorted(label_path)
                    for index1 , file_name1 in enumerate(label_path):
                        label.append(os.path.join(self.transfer.training_path,file,file1,label_path[index1]))
                            

        img = sorted(img)
        label = sorted(label)
        meta_data['img_dir']=img
        meta_data['label_dir']=label


        meta_data_c = ConfigBox(meta_data)
        img_dir = sorted(meta_data_c.img_dir)
        label_dir = sorted(meta_data_c.label_dir)

        overwrite_flag = self.transfer.overwrite
        
        for (index, img_data), (index1, label_data) in zip(enumerate(img_dir), enumerate(label_dir)):
            # folder_name = img_data.split('training')[1].split('\\')[1]
            folder_name = img_data.split('training')[1].split('/')[1]
            original_data = os.path.join(self.transfer.org_path, folder_name)
            label_data_test = os.path.join(self.transfer.mask_path, folder_name)
            
            os.makedirs(original_data, exist_ok=True)
            os.makedirs(label_data_test, exist_ok=True)
            shutil.copy(img_data, original_data)
            shutil.copy(label_data, label_data_test)
            logging.info(f'Data Transfer {img_data} => {original_data}')
            logging.info(f'Data Transfer {label_data} => {label_data_test}')


            # if overwrite_flag:
            #     shutil.copy(img_data, original_data)
            #     shutil.copy(label_data, label_data_test)
            #     logging.info('Data Already exists, Overwriting')
            # else:
            #     if os.path.getsize(original_data) == 0 and os.path.getsize(label_data_test) == 0:
            #         shutil.copy(img_data, original_data)
            #         shutil.copy(label_data, label_data_test)
            #     else:
            #         logging.info('Data Already exists, Skipping')
                    

        end = time.time() - start
        logging.info(end)
        logging.info('Complete data copied')
        logging.info(f'{"*" *20} Data Transfer stage completed {"*"*20}')
        logging.info(f'Total time taken for Execution -->{end}')



              
