from src.checkout.entity import Modelevaluationconfig
from ultralytics import YOLO
import os
from pathlib import Path
import pandas as pd
import time

class Modelevalution:
    def __init__(self, Modelevalutionconfig= Modelevaluationconfig):
        self.config = Modelevalutionconfig
        self.curdir = Path(os.getcwd())

    
    def evaluation(self):
        train_img_path = self.config.modelMetaData
        model = YOLO("models/best.pt")
        all_predictions = []
        for folder in sorted(os.listdir(train_img_path)):
            listimages = []
            # Define the directory path
            directory = folder
            # Get a list of files in the directory
            files = os.listdir(os.path.join(self.curdir,train_img_path,folder))
            # Create a list of tuples containing filename and size
            file_sizes = [(file, os.path.getsize(os.path.join(self.curdir,train_img_path,directory, file))) for file in files]

            # Sort the list by file size in ascending order (bottom 5)
            file_sizes.sort(key=lambda x: x[1])

            # Get the bottom 5 files
            bottom_5 = file_sizes[:5]

            # Sort the list by file size in descending order (top 5)
            file_sizes.sort(key=lambda x: x[1], reverse=True)

            # Get the top 5 files
            top_5 = file_sizes[:5]

            # Calculate the average file size
            total_size = sum(size for _, size in file_sizes)
            average_size = total_size / len(file_sizes)

            # Sort the list by the absolute difference between file size and average size
            file_sizes.sort(key=lambda x: abs(x[1] - average_size))

            # Get the 5 files with sizes closest to the average
            average_files = file_sizes[:5]

            # Print the top 5 and bottom 5 files
            # print("Top 5 files by size:")
            for file, size in top_5:
                each_img = os.path.join(self.curdir,train_img_path,folder,file)
                # print(f"{each_img}: {size} bytes")
                listimages.append(each_img)

            # print("\nBottom 5 files by size:")
            for file, size in bottom_5:
                each_img = os.path.join(self.curdir,train_img_path,folder,file)
                # print(f"{each_img}: {size} bytes")
                listimages.append(each_img)

            # Print the 5 files with average size
            # print("5 files with sizes closest to the average:")
            for file, size in average_files:
                each_img = os.path.join(self.curdir,train_img_path,folder,file)
                # print(f"{each_img}: {size} bytes")
                listimages.append(each_img)

            try:
                for each_img in listimages:
                    # print(f' ========== {each_img} ==========')
                    # Pass the image through the YOLO model
                    # results = model(each_img, save=True, imgsz=640, conf=0.1, device="1", save_txt=True, visualize=True)
                    results = model(each_img, save=True, imgsz=640, conf=0.1, device="0")
                    # Get the top prediction
                    top_prediction = None
                    unique_classes = set()
                    for i, box in enumerate(results[0].boxes):
                        class_id = results[0].names[box.cls[0].item()]
                        conf = round(box.conf[0].item(), 2)
                        cords = box.xyxy[0].tolist()
                        cords = [round(x, 2) for x in cords]
                        unique_classes.add(class_id)
                        if top_prediction is None or conf > top_prediction[1]:
                            top_prediction = (class_id, conf, cords)

                    # Prepare the JSON response
                    if top_prediction is not None:
                        # Single class detected, return prediction of that class
                        class_id, conf, cords = top_prediction
                        prediction = {
                            "item_name": folder,
                            "Intances detected": len(results[0].boxes),
                            "pred_class": class_id,
                            "pred_confidence": conf,
                            "captured_image_path": each_img
                        }
                        all_predictions.append(prediction)  # Add the prediction to the list
            except Exception as e:
                print(f"An error occurred: {e}")
                # You can handle other exceptions here
                continue
            else:
                print("Evaluation loop completed successfully")
        # Create a DataFrame from the selected data
        df = pd.DataFrame(all_predictions)
        
        #Define output directory
        output_file_dir = 'artifacts/outputs'
        
        # Define the path where you want to save the CSV files
        output_file_name = f'output_predictions{time.time()}.csv'
        
        #Output directory to store csv files
        os.makedirs(output_file_dir,exist_ok=True)

        output_csv_path = Path(os.path.join(output_file_dir, output_file_name))
        
        # Save the DataFrame to a CSV file
        df.to_csv(output_csv_path, index=False)
