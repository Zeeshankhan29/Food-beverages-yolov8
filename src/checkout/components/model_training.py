from src.checkout.entity import ModelTrainingConfig
import os
import sys
from pathlib import Path
from ultralytics import YOLO
# from clearml import Task
import shutil
import yaml
from src.checkout import logging
import argparse
from box import ConfigBox
import time

class ModelTraining:
    def __init__(self, ModelTrainingConfig=ModelTrainingConfig):
        self.modeltraining = ModelTrainingConfig
        self.curr_dir = Path(os.getcwd())
        self.yolo_config_dir = Path(self.modeltraining.yolo_config_dir)
        self.params_path = os.path.join(self.curr_dir, 'params.yaml')
        
        #Define the project name and task
        # self.task = Task.init(project_name="Segmentation",task_name="Model 3.0 release")

    def yolo_train(self):
        '''Epochs value depends on the accuracy required, the more the epoch the more the accuracy'''

        logging.info('-'*20 +f"Model Training stage Completed " +'-'*20)
        

        # # Log "model_variant" parameter to task
        # self.task.set_parameter("model_variant", 'best')

        self.yolo_config_dir1 = Path(os.path.join(self.curr_dir, self.yolo_config_dir))

        '''Loading the YOLO config file'''
        self.yolo_config_path1 = Path(os.path.join(self.yolo_config_dir1, 'train.yaml'))

        logging.info('-' * 20 + f"Model Training stage started " + '-' * 20)
        logging.info(f'Data training from {self.yolo_config_path1} directory')

        # Load parameters from YAML file or use default values
        yaml_params = {}
        if os.path.exists(self.params_path):
            with open(self.params_path, 'r') as params_file:
                yaml_params = yaml.safe_load(params_file) or {}

        # Define default parameter values
        default_params = {
            "model_variant" : 'yolov8n-seg.pt',
            "batch": 32,
            "epochs": 100,
            "imgsz": 416,
            "device": "cuda",
            "verbose": False,
            "cos_lr": False,
            "optimizer": "Adam",
            "patience": 10,
            "workers": 4,
            "nbs": 64,
            "val": True,
            "mask_ratio": 0.5,
            "lr0": 0.001,
            "lrf": 0.1
        }

        # Merge default and YAML parameters
        merged_params = {**default_params, **yaml_params}

        # Create a ConfigBox for parameter access
        args = ConfigBox(merged_params)
        
        #Load required model varaint
        model = YOLO(args.model_variant)
        
        # print(args)
        
        model.train(
            # data=self.yolo_config_path1,
            data="/media/visionai/DATA11/trainingdata-classify/classifydata-640/Originals-0",
            name = args.name,
            batch=args.batch,
            epochs=args.epochs,
            imgsz=args.imgsz,
            device=args.device,
            verbose=args.verbose,
            cos_lr=args.cos_lr,
            optimizer=args.optimizer,
            patience=args.patience,
            workers=args.workers,
            nbs=args.nbs,
            val=args.val,
            mask_ratio=args.mask_ratio,
            lr0=args.lr0,
            lrf=args.lrf
        )

        #Create key word arguments for Clearml
        # args1 = dict(data=self.yolo_config_path1,
        #     batch=args.batch,
        #     epochs=args.epochs,
        #     imgsz=args.imgsz,
        #     device=args.device,
        #     verbose=args.verbose,
        #     cos_lr=args.cos_lr,
        #     optimizer=args.optimizer,
        #     patience=args.patience,
        #     workers=args.workers,
        #     nbs=args.nbs,
        #     val=args.val,
        #     mask_ratio=args.mask_ratio,
        #     lr0=args.lr0,
        #     lrf=args.lrf)
        
        # # Passing the parameters to clearml 
        # self.task.connect(args1)

        # #Add results to Clearml for tracing purposes
        # results = model.train(**args1)
        
        logging.info('-' * 20 + f"Model Training stage Completed " + '-' * 20)
