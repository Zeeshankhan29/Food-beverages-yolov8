import cv2
import os
import re
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS , cross_origin
from ultralytics import YOLO
import pandas as pd
import schedule
import mysql.connector as cn 
import numpy as np
import time
import torch
import torchvision
import torchvision.io
import concurrent.futures
import threading
from collections import Counter
import yaml
from PIL import Image

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'

# log directory
log_path = 'predict.log'

#Load Models configuration 
with open('floraconfig.yaml','r') as config:
    config = yaml.safe_load(config)

#Load Items Id's
with open('items.yaml', 'r') as params_file:
    yaml_params = yaml.safe_load(params_file) or {}

#Load Reliance Items Id's
# with open('items-reliance.yaml', 'r') as params_file:
#     yaml_params = yaml.safe_load(params_file) or {}

# Ensure that the "capture" folder exists
os.makedirs("capture", exist_ok=True)
os.makedirs("classfnvmodel", exist_ok=True)


# Set up logging
log_format = '[%(asctime)s] : [%(name)s] : [%(levelname)s] :[%(message)s]'
logging.basicConfig(filename=log_path , level=logging.DEBUG, format=log_format)
stream = logging.StreamHandler()
log = logging.getLogger()
log.addHandler(stream)

# Load the YOLO model
logging.info("Loading AI model...")
models1 = YOLO(config['Model_M1']['save_path'])
models2 = YOLO(config['Model_M2']['save_path'])
modelc1 = YOLO(config['model_variant']['save_path'])
logging.info("AI model loaded successfully.")


# Initialize the camera
camera = cv2.VideoCapture(0)  # Use appropriate camera index if multiple cameras are available


@app.route('/', methods=['POST'])
def capture_image():
    ret, frame = camera.read()
    return frame


def insert_items_to_db():
    with open('items.yaml', 'r') as params_file1:
        yaml_params1 = yaml.safe_load(params_file1) or {}
    df = pd.DataFrame({'Item_id':yaml_params1.values(),'Item_name': yaml_params1.keys(),'model_type' : 'Segmentation','model_version':'v1.0'})
    try:
        mydb=cn.connect(host='localhost',user='root',passwd='Snzk@#1329')
        cursor=mydb.cursor()
        cursor.execute('create database checkout')
        cursor.execute('use checkout')
        cursor.execute('CREATE TABLE if not EXISTS  vendors(Item_id int, Item_name varchar(100) primary key,model_type varchar(100), model_version varchar(100), DateTime1 DATETIME DEFAULT NOW())')
        for i,row in df.iterrows():
            cursor.execute('insert into vendors values (%s,%s,%s,%s,NOW())',tuple(row))
        mydb.commit()
        logging.info('Database updated successfully')
    except:
        mydb=cn.connect(host='localhost',user='root',passwd='Snzk@#1329')
        cursor=mydb.cursor()
        cursor.execute('use checkout')
        df1 = pd.read_sql('select * from vendors',mydb)
        if len(df) != len(df1):
            new_items = df['Item_name']
            exist_items = df1['Item_name']
            set1 = set(exist_items)
            set2 = set(new_items)
            value11 = list(set2.difference(set1))
            df2 = df[df['Item_name'].isin(value11)]
            for i,row in df2.iterrows():
                cursor.execute('insert into vendors values (%s,%s,%s,%s,NOW())',tuple(row))
            mydb.commit()
            logging.info('Database updated successfully')
        else:
            logging.info('No Changes found in the Metadata, skipping Database updation')
    
    # Schedule the task to run every day at 12 am
schedule.every(5).minutes.do(insert_items_to_db)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

target_func = threading.Thread(target=run_schedule)
target_func.start()

@app.route('/', methods=['POST'])
def pass_img():
    files = request.files.get('img_path')
    stream_file = Image.open(files.stream)
    arr = np.array(stream_file)
    rgb_img = cv2.cvtColor(arr,cv2.COLOR_BGR2RGB)
    return rgb_img

@app.route('/metadata', methods=['POST'])
def meta():
    try:
        # Load Models configuration 
        global config
        image = capture_image()
        # image = pass_img()
        image_path = os.path.join(os.getcwd(),f"capture", f"captured_image{int(time.time())}.png")
        cv2.imwrite(image_path, image)
        logging.info('saving the captured image to: %s', image_path)

        # Create threads for each model
        thread_m1 = threading.Thread(target=process_model, args=(models1, config['Model_M1'], image_path))
        thread_m2 = threading.Thread(target=process_model, args=(models2, config['Model_M2'], image_path))

        # Start the threads
        thread_m1.start()
        thread_m2.start()

        # Wait for threads to finish
        thread_m1.join()
        thread_m2.join()

        # Retrieve metadata from each model
        metadata_m1 = thread_m1.result
        metadata_m2 = thread_m2.result

        logging.info(f'Model_M1 metadata : {metadata_m1}')
        logging.info(f'Model_M2 metadata : {metadata_m2}')

        return jsonify({'Model_M1 metadata': metadata_m1, 'Model_M2 metadata': metadata_m2})

    except Exception as e:
        logging.exception('Something went wrong. Please check logs.')

def process_model(model, model_config, image_path):
    try:
        # Pass the image through the YOLO model
        results = model(image_path, save=model_config['save_img'], imgsz=model_config['img_size'], conf=model_config['confidence'])
        metadata = results[0].names
        logging.info(f'Model metadata : {metadata}')

        # Store the metadata in the thread's result attribute
        threading.current_thread().result = metadata

    except Exception as e:
        logging.exception('Error processing model.')
        threading.current_thread().result = None

@app.route('/predict', methods=['POST'])
def predict_image():
        global config
        global models1
        global models2
        global modelc1
        global yaml_params
        if config['model_variant']['model_type'] =='Segmentation':
            try:
                #Load Models configuration 
                # image = pass_img()
                image = capture_image()
                image_path = os.path.join(os.getcwd(),f"capture", f"captured_image{int(time.time())}.png")
                cv2.imwrite(image_path, image)
                logging.info('saving the captured image to: %s', image_path)
                
                # Pass the image through the YOLO model
                results = models1(image_path, save=config['Model_M1']['save_img'], imgsz=config['Model_M1']['img_size'], conf=config['Model_M1']['confidence'])

                results1 = models2(image_path, save=config['Model_M2']['save_img'], imgsz=config['Model_M2']['img_size'], conf=config['Model_M2']['confidence'])

                # Get the top prediction
                predict = []
                top_prediction = None
                unique_classes = set()
                filtered = []
                for i, box in (enumerate(results[0].boxes)):
                    class_id = results[0].names[box.cls[0].item()]
                    conf = round(box.conf[0].item(), 2)
                    # cords = box.xyxy[0].tolist()
                    # cords = [round(x, 2) for x in cords]
                    unique_classes.add(class_id)
                    filtered.append({
                        'class_id': class_id,
                        'confidence': conf,

                    })
            
                if filtered:
                    value = Counter(item['class_id'] for item in filtered)
                    count_f = sorted(filtered,key=lambda x: value[x['class_id']],reverse=True)
                    top_3 = count_f[:3]
                    top_pred_f = sorted(top_3,key=lambda x: -x['confidence'])   
                    top_prediction = top_pred_f[:1] 
                    print(f">>>>>>>>>>{top_prediction}")
                else:
                    logging.info(f"No prediction detected in best.pt")
                    return jsonify({"error": "No prediction detected"}), 200

                unique_classes1 = set()
                top_prediction1 = None
                filtered1 = []
                for i, box1 in (enumerate(results1[0].boxes)):
                    class_id1 = results1[0].names[box1.cls[0].item()]
                    conf1 = round(box1.conf[0].item(), 2)
                    # cords1 = box1.xyxy[0].tolist()
                    # cords1 = [round(x, 2) for x in cords1]
                    unique_classes1.add(class_id1)
                    filtered1.append({
                        'class_id': class_id1,
                        'confidence': conf1
                    })
                
                if filtered1:
                    value1 = Counter(item1['class_id'] for item1 in filtered1)
                    count_f1 = sorted(filtered1,key=lambda x: value1[x['class_id']],reverse=True)
                    top_31 = count_f1[:3]
                    top_pred_f1 = sorted(top_31,key=lambda x: -x['confidence'])   
                    top_prediction1 = top_pred_f1[:1] 
                    print(f">>>>>>>>>>{top_prediction1}")
                else:
                    logging.info(f"No prediction detected in last.pt")
                    return jsonify({"error": "No prediction detected"}), 200


            
                if len(unique_classes) <= 2  or len(unique_classes1) <= 2 :
                    #Model M1
                    class_id = top_prediction[0]['class_id']
                    conf = top_prediction[0]['confidence']
                    
                    #Model M2
                    class_id1 = top_prediction1[0]['class_id']
                    conf1 = top_prediction1[0]['confidence']
            

                    if class_id == class_id1:
                        predict.append({
                        'item_id' :yaml_params[class_id],
                        'model_id':config['Model_M1']['type'],
			            'predict_class': class_id,
                        "captured_image_path": image_path,
                        "pred_confidence": conf,
                        "unique_items_count": len(results[0].boxes),
                        "timestamp": time.ctime(time.time())
                        })
                        
                    if class_id != class_id1:
                        predict.append({
                        'model_id':config['Model_M1']['type'],
                        'item_id' :yaml_params[class_id],
                        'predict_class': class_id,
                        "captured_image_path": image_path,
                        "pred_confidence": conf,
                        "unique_items_count": len(results[0].boxes),
                        "timestamp": time.ctime(time.time())
                        })
                        predict.append({
                        'model_id': config['Model_M2']['type'],
                        'item_id' :yaml_params[class_id1],
                        'predict_class' : class_id1,
                        "captured_image_path": image_path,
                        "pred_confidence": conf1,
                        "unique_items_count": len(results1[0].boxes),
                        "timestamp": time.ctime(time.time())

                        })

                        
                    
                            
                else:
                    # Multiple classes detected, return "Mixed Fruit" with confidence
                    predict.append({
                        "captured_image_path": image_path,
                        "unique_items_count": len(unique_classes),
                        "pred_class": "Mixed Fruit",
                        "item_id": -1,
                        "pred_confidence": max([box.conf[0].item() for box in results[0].boxes]),
                        "timestamp": time.ctime(time.time())
                        
                    })
                        
                    

                
                # Log the prediction to the file and console
                logging.info(f"Predictions---->{predict}")

                return jsonify({'predictions':predict})
            
            
            except Exception as e:
                # Catch any exception that occurs during execution and log it
                error_msg = "An error occurred during prediction: " + str(e)
                logging.exception(error_msg)
                return jsonify({"error": "An error occurred during prediction."}), 200

        if config['model_variant']['model_type'] == 'Classification':
            try:
                #Load Classification configuration 
                # image = pass_img()
                image = capture_image()
                resized_image = cv2.resize(image,(config['model_variant']['img_width'],config['model_variant']['img_height']))
                image_path = os.path.join(os.getcwd(),f"capture", f"captured_image{int(time.time())}.png")
                cv2.imwrite(image_path, resized_image)
                logging.info('saving the captured image to: %s', image_path)

                # model = YOLO(config['model_variant']['save_path'])
                # Pass the image through the YOLO model
                results = modelc1(image_path, save=config['model_variant']['save_img'])
                
                detect = []
                predictions = []
                # Process results list
                for result in results:
                    for value,confd in zip(result.probs.top5,result.probs.top5conf):
                        class_name = result.names[value]
                        confidence = round(float(confd.numpy()),2)
                        detect.append(
                            (class_name,confidence)
                        )
                    if detect:
                        sorted_detect = sorted(detect, key=lambda x: -x[1])
                        # if sorted_detect[0][1] >= 90.00:
                        #     class_name = sorted_detect[0][0]
                        #     conf = sorted_detect[0][1]
                        #     predictions.append({
                        #         'model_id': config['model_variant']['type'],
                        #         "item_id" : yaml_params[class_name],
                        #         'predict_class': class_name,
                        #         "captured_image_path": image_path,
                        #         "pred_confidence": conf,
                        #         "timestamp": time.ctime(time.time())}

                        #     )

                        if sorted_detect[0][1] < 90.00:
                            class_name1 = sorted_detect[0][0]
                            conf1 = sorted_detect[0][1]
                            predictions.append({
                                'model_id': config['model_variant']['type'],
                                "item_id" : yaml_params[class_name1],
                                'predict_class': class_name1,
                                "captured_image_path": image_path,
                                "pred_confidence": conf1,
                                "timestamp": time.ctime(time.time())}

                            )
                            class_name2 = sorted_detect[1][0]
                            conf2 = sorted_detect[1][1]
                            predictions.append({
                                'model_id': config['model_variant']['type'],
                                "item_id" : yaml_params[class_name2],
                                'predict_class': class_name2,
                                "captured_image_path": image_path,
                                "pred_confidence": conf2,
                                "timestamp": time.ctime(time.time())}

                            )
                            class_name3 = sorted_detect[2][0]
                            conf3 = sorted_detect[2][1]
                            predictions.append({
                                'model_id': config['model_variant']['type'],
                                "item_id" : yaml_params[class_name3],
                                'predict_class': class_name3,
                                "captured_image_path": image_path,
                                "pred_confidence": conf3,
                                "timestamp": time.ctime(time.time())}

                            )
                            class_name4 = sorted_detect[3][0]
                            conf4 = sorted_detect[3][1]
                            predictions.append({
                                'model_id': config['model_variant']['type'],
                                "item_id" : yaml_params[class_name4],
                                'predict_class': class_name4,
                                "captured_image_path": image_path,
                                "pred_confidence": conf4,
                                "timestamp": time.ctime(time.time())}

                            )
                            class_name5 = sorted_detect[4][0]
                            conf5 = sorted_detect[4][1]
                            predictions.append({
                                'model_id': config['model_variant']['type'],
                                "item_id" : yaml_params[class_name5],
                                'predict_class': class_name5,
                                "captured_image_path": image_path,
                                "pred_confidence": conf5,
                                "timestamp": time.ctime(time.time())}

                            )
                 # Log the prediction to the file and console
                logging.info(f"Predictions---->{predictions}")

                return jsonify({'predictions':predictions})
            except Exception as e:
                 # Catch any exception that occurs during execution and log it
                error_msg = "An error occurred during prediction: " + str(e)
                logging.exception(error_msg)
                return jsonify({"error": "An error occurred during prediction."}), 200



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3598)
