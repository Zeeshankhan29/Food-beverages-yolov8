from src.checkout.entity import DataIngestionConfig, ModelTrainingConfig
import os
import sys
from pathlib import Path
from ultralytics import YOLO
import os
import cv2
import shutil
from src.checkout import logging
from src.checkout.utils import read_yaml
import re
import pprint


class DataIngestion:
    def __init__(self, DataIngestionConfig=DataIngestionConfig):
        self.dataingestion = DataIngestionConfig
        self.curr_dir = Path(os.getcwd())
        self.temp_mask_dir = Path(self.dataingestion.temp_mask_dir)
        self.temp_labels_dir = Path(self.dataingestion.temp_labels_dir)
        self.temp_original_dir = Path(self.dataingestion.original_image_dir)
        self.yolo_config = Path(self.dataingestion.yolo_seg_config_file)
    
    def resize_img(self, target_width=640):
        for file in sorted(os.listdir(self.temp_original_dir)):
            ab_path = Path(os.path.join(self.curr_dir, self.temp_original_dir))
            file_path = Path(os.path.join(ab_path, file))
            for each_file in os.listdir(file_path):
                file_path1 = Path(os.path.join(file_path, each_file))

                if file_path1.is_file():
                    image = cv2.imread(str(file_path1))
                    if image is not None:
                        original_height, original_width, _ = image.shape
                        target_height = int(
                            (target_width / original_width) * original_height)

                        if image.shape[1] == target_width and image.shape[0] == target_height:
                            logging.info(
                                f"Skipped (already resized): {file} - {each_file}")
                            continue

                        resized_image = cv2.resize(
                            image, (target_width, target_height))
                        cv2.imwrite(str(file_path1), resized_image)
                        logging.info(f"Resized: {file} - {each_file}")
                    else:
                        logging.info(f"Failed to read: {file}  - {each_file}")
        

        for file1 in sorted(os.listdir(self.temp_mask_dir)):
            ab_path1 = Path(os.path.join(self.curr_dir, self.temp_mask_dir))
            file_path1 = Path(os.path.join(ab_path1, file1))
            for each_file1 in os.listdir(file_path1):
                file_path2 = Path(os.path.join(file_path1, each_file1))

                if file_path2.is_file():
                    image = cv2.imread(str(file_path2))
                    if image is not None:
                        original_height, original_width, _ = image.shape
                        target_height = int(
                            (target_width / original_width) * original_height)

                        if image.shape[1] == target_width and image.shape[0] == target_height:
                            logging.info(
                                f"Skipped (already resized): {file1}  - {each_file1}")
                            continue

                        resized_image = cv2.resize(
                            image, (target_width, target_height))
                        cv2.imwrite(str(file_path2), resized_image)
                        logging.info(f"Resized: {file1} - {each_file1}")
                    else:
                        logging.info(f"Failed to read: {file1} - {each_file1}")
                else:
                    logging.info(f"Failed to read: {file1} - {each_file}")


    def data_valid(self):
        for file in sorted(os.listdir(self.temp_original_dir)):
            file_path = os.path.join(
                self.curr_dir, self.temp_original_dir, file)
            for file_name in sorted(os.listdir(file_path)):
                if not file_name.endswith('.png'):
                    unwanted_file_path = os.path.join(file_path, file_name)
                    try:
                        os.remove(unwanted_file_path)
                        logging.info(
                            f'Removing file {file_name} from {file} class')
                    except:
                        shutil.rmtree(unwanted_file_path)
                        logging.info(
                            f'Removing file {file_name} from {file} class')

        for file1 in sorted(os.listdir(self.temp_mask_dir)):
            file_path1 = os.path.join(self.curr_dir, self.temp_mask_dir, file1)
            for file_name1 in sorted(os.listdir(file_path1)):
                if not file_name1.endswith('.png') or file_name1.startswith('.ipynb'):
                    unwanted_file_path1 = os.path.join(file_path1, file_name1)
                    try:
                        os.remove(unwanted_file_path1)
                        logging.info(
                            f'Removing file {file_name1} from {file1} class')
                    except:
                        shutil.rmtree(unwanted_file_path1)
                        logging.info(
                            f'Removing file {file_name1} from {file1} class')

    def data_counter(self):
        image_path = []
        annot_path = []
        datatraining = read_yaml(self.yolo_config)
        classnames = datatraining.names
        
        #Selected class names length
        for classname in classnames:
            for images, annot in zip(sorted(os.listdir(self.temp_original_dir)), sorted(os.listdir(self.temp_mask_dir))):
                if classname in images:
                    image_path.append(os.path.join(
                        self.curr_dir, self.temp_original_dir, images))
                    annot_path.append(os.path.join(
                        self.curr_dir, self.temp_mask_dir, annot))

        for img_path, label_path in zip(image_path, annot_path):
            file_name = os.path.basename(img_path)
            label_name = os.path.basename(label_path)
            if len(os.listdir(img_path)) != len(os.listdir(label_path)):
                logging.info('Criticial error detected ')
                logging.info("Original image and Mask labels doesn't match")
                logging.info("Stopped Execution>>>>>>>>>>>>>>>>")
                logging.info(
                    f"{file_name} original folder has {len(os.listdir(img_path))}")
                logging.info(
                    f"{label_name} mask folder has {len(os.listdir(label_path))}")
                exit(0)

            else:
                logging.info('\n')
                logging.info(f'{file_name}, --->{len(os.listdir(img_path))}')
                logging.info(
                    f'{label_name}, --->{len(os.listdir(label_path))}')
                logging.info('\n')

    def yolo_polygon_to_label1(self):
        # print(self.datatraining.names)

        datatraining = read_yaml(self.yolo_config)
        classnames = datatraining.names
        datasetMetaData = []
    
        for j in sorted(os.listdir(self.temp_mask_dir)):
            if j in classnames:
                image_path = Path(os.path.join(self.temp_mask_dir, j))
                mask_files = []
                original_files = []
                label_files = []
                label_class = ""
                label_index = 0
                if image_path.is_dir():  # Check if the full path is a directory

                    absolute_mask_dir = os.path.join(
                        self.curr_dir, self.temp_mask_dir, j)

                    absolute_original_dir = os.path.join(
                        self.curr_dir, self.temp_original_dir, j)

                    absolute_lable_dir = os.path.join(
                        self.curr_dir, self.temp_labels_dir, j)
                    for index, classname in enumerate(classnames):
                        # print(f'{index} = {classname}')
                        txt = str(absolute_mask_dir)
                        # Use re.findall() to find all occurrences of the pattern
                        matches = re.findall("([\\\/]"+str(classname)+")$", txt)
                        # Get the count of occurrences
                        count = len(matches)
                        if count > 0:
                            label_class = str(classname)
                            label_index = index
                            break

                    folder_name = j  # Use the directory name as the folder name

                    # Create the destination directory path
                    file_dir = os.path.join(self.temp_labels_dir, folder_name)
                    os.makedirs(file_dir, exist_ok=True)

                    # Iterate over files in the directory
                    tmpFiles = []
                    for files in sorted(os.listdir(image_path)):
                        file_path = os.path.join(image_path, files)
                        if os.path.isfile(os.path.join(
                                self.curr_dir, file_path)) and os.path.exists(os.path.join(
                                self.curr_dir, file_path)):  # Check if the current item is a file
                            tmpFiles.append(os.path.basename(str(file_path)))
                            labelfile = os.path.join(absolute_lable_dir, os.path.basename(
                                str(file_path).replace(".png", ".txt")))

                            if not os.path.exists(labelfile):
                                # Load the binary mask and get its contours
                                mask = cv2.imread(os.path.join(
                                    self.curr_dir, file_path), cv2.IMREAD_GRAYSCALE)

                                _, mask = cv2.threshold(
                                    mask, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

                                H, W = mask.shape
                                contours, hierarchy = cv2.findContours(
                                    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                                # Convert the contours to polygons
                                polygons = []
                                for cnt in contours:
                                    if cv2.contourArea(cnt) > 200:
                                        polygon = []
                                        for point in cnt:
                                            x, y = point[0]
                                            polygon.append(x / W)
                                            polygon.append(y / H)
                                        polygons.append(polygon)

                                # Print the polygons to the respective label files
                                # output_file_path = os.path.join(
                                #    file_dir, "{}.txt".format(files[:-4]))
                                output_file_path = labelfile
                                with open(output_file_path, 'w') as f:
                                    for polygon in polygons:
                                        for p_, p in enumerate(polygon):
                                            if p_ == len(polygon) - 1:
                                                f.write('{}\n'.format(round(p,4)))
                                            elif p_ == 0:
                                                f.write(str(label_index) +
                                                        ' {} '.format(round(p,4)))
                                            else:
                                                f.write('{} '.format(round(p,4)))
                    tmpFiles = sorted(tmpFiles)
                    for fn in tmpFiles:
                        mask_files.append(os.path.join(
                            absolute_mask_dir, fn))
                        original_files.append(os.path.join(
                            absolute_original_dir, fn))
                        label_files.append(os.path.join(
                            absolute_lable_dir, fn.replace(".png", ".txt")))
                    datasetMetaData.append({
                        "classname": str(label_class),
                        "classindex": str(label_index),
                        "mask_dir": absolute_mask_dir,
                        "original_dir": absolute_original_dir,
                        "label_dir": absolute_lable_dir,
                        "mask_files": mask_files,
                        "mask_files_len": len(mask_files),
                        "original_files": original_files,
                        "original_files_len": len(original_files),
                        "label_files": label_files,
                        "label_files_len": len(label_files)
                    })

                logging.info(
                    "-" * 20 + f'Data Ingestion stage started for {folder_name}' + "-" * 20)
                logging.info(
                    f'loading mask images  for {folder_name} at directory {self.temp_mask_dir} ')
                logging.info(
                    f'creating the output path for {folder_name} at directory {file_dir}')
                logging.info(f'Reading each files from {folder_name} folder')
                logging.info(
                    f'Iterating over the files in the directory {image_path} for {folder_name}')
                logging.info(f'Finding the polygon for each {folder_name} image')
                logging.info(
                    f'Storing the polygon for each {folder_name} image at directory {file_dir}')
                logging.info(
                    "-" * 20 + f'Data Ingestion stage completed for {folder_name}' + "-" * 20)
        return datasetMetaData

   