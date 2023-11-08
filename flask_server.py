import cv2
import os
import re
import logging
from flask import Flask, jsonify, request
from ultralytics import YOLO
import numpy as np
import time
import torch
import torchvision
import torchvision.io
import warnings
from box import ConfigBox
import yaml

app = Flask(__name__)

# Set up logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

# Create a file handler for prediction logs
predict_log_file = logging.FileHandler('predict.log')
predict_log_file.setLevel(logging.INFO)
predict_log_file.setFormatter(logging.Formatter(log_format))

# Add the file handlers to the root logger
logging.getLogger().addHandler(predict_log_file)

# Load the YOLO model
logging.info("Loading AI model...")
model = YOLO("models/best.pt")
logging.info("AI model loaded successfully.")

# Ensure that the "capture" folder exists
os.makedirs("capture", exist_ok=True)

# Initialize the camera
camera = cv2.VideoCapture(0)  # Use appropriate camera index if multiple cameras are available


@app.route('/', methods=['POST'])
def capture_image():
    ret, frame = camera.read()
    return frame
# Create a list to store predictions for logging
all_predictions = []

@app.route('/predict', methods=['POST'])
def predict_image():
    try:
        # Save the captured image to the "capture" folder
        image = capture_image()
        image_path = os.path.join(f"capture", f"captured_image{int(time.time())}.jpg")
        cv2.imwrite(image_path, image)
        logging.info('saving the captured image to: %s', image_path)
        image1 = f'captured_image{int(time.time())}.jpg'
        image2 = os.path.join('capture',image1)

        # Pass the image through the YOLO model
        results = model(image2, save=True, imgsz=640, conf=0.9)

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
            if len(unique_classes) == 1:
                with open('items.yaml', 'r') as params_file:
                    yaml_params = yaml.safe_load(params_file) or {}
                # Single class detected, return prediction of that class
                class_id, conf, cords = top_prediction
                prediction = {
                    "captured_image_path": image_path,
                    "predictions": {
                        "unique_items_count": len(results[0].boxes),
                        "items": [
                            {
                                "pred_class": class_id,
                                "item_id" : yaml_params[class_id],
                                "pred_confidence": conf,
                                "bounding_box": cords
                            }
                        ]
                    },
                    "metadata": {
                        "names": results[0].names
                    }
                }
            else:
                # Multiple classes detected, return "Mixed Fruit" with confidence
                prediction = {
                    "captured_image_path": image_path,
                    "predictions": {
                        "unique_items_count": len(unique_classes),
                        "items": [
                            {
                                "pred_class": "Mixed Fruit",
                                "item_id": -1,
                                "pred_confidence": max([box.conf[0].item() for box in results[0].boxes]),
                                "bounding_box": []
                            }
                        ]
                    },
                    "metadata": {
                        "names": results[0].names
                    }
                }

            all_predictions.append(prediction)  # Add the prediction to the list

            # Log the prediction to the file
            logging.info("Prediction: %s", prediction)

            # Print the prediction on the console
            logging.info("Prediction:", prediction)

            return jsonify(prediction)
        logging.info("No prediction detected.")
        return jsonify({"error": "No prediction detected."}), 500
    
    except Exception as e:
        # Catch any exception that occurs during execution and log it
        error_msg = "An error occurred during prediction: " + str(e)
        logging.error(error_msg)
        return jsonify({"error": "An error occurred during prediction."}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3598)
