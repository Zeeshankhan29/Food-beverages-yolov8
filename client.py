# import cv2
# import requests
# import base64

# def capture_and_predict():
#     # Capture an image from the camera
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     cap.release()

#     # Convert the image to a data URL
#     _, img_encoded = cv2.imencode('.png', frame)
#     img_str = base64.b64encode(img_encoded.tobytes()).decode('utf-8')
#     data_url = f'data:image/png;base64,{img_str}'

#     # Send the image to the Flask server
#     url = 'http://192.168.2.109:3598/predict'  # Change the URL accordingly
#     payload = {'image': data_url}
#     response = requests.post(url, json=payload)

#     # Print or process the prediction results
#     print(response.json())

# if __name__ == "__main__":
#     capture_and_predict()

import cv2
from flask import Flask,jsonify
import requests
import base64
import threading
import time

app = Flask(__name__)
camera = cv2.VideoCapture(0)
frame = None
lock = threading.Lock()

def capture_frames():
    global frame
    while True:
        ret, current_frame = camera.read()
        with lock:
            frame = current_frame.copy()  # Make a copy to avoid interference with capturing
        time.sleep(0.1)  # Adjust the delay between frames as needed

@app.route('/start_capture', methods=['POST'])
def start_capture():
    threading.Thread(target=capture_frames, daemon=True).start()
    return jsonify({'message': 'Camera capture started.'})

@app.route('/capture_and_predict', methods=['POST'])
def capture_and_predict():
    with lock:
        captured_frame = frame

    if captured_frame is not None:
        # Convert the image to a data URL
        _, img_encoded = cv2.imencode('.png', captured_frame)
        img_str = base64.b64encode(img_encoded.tobytes()).decode('utf-8')
        data_url = f'data:image/png;base64,{img_str}'

        # Send the image to the Flask server
        url = 'http://192.168.2.109:3598/predict'  # Change the URL accordingly
        payload = {'image': data_url}
        response = requests.post(url, json=payload)

        # Print or process the prediction results
        print(response.json())
        prediction_result = response.json()
        return jsonify({'prediction_result': prediction_result})

    return jsonify({'message': 'Image sent for prediction.'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3598, threaded=True)
