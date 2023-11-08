import streamlit as st
import numpy as np
import cv2
import torch
from torchvision import transforms
from PIL import Image
from io import BytesIO
from ultralytics import YOLO



model = YOLO('last.pt')
# results = model.predict(source=r'C:\Users\Zeeshan.khan\vscode_projects\checkout\Kiwi Imported Green_10-31-2022-14-57-0258028_Focus_38.png',save=True,imgsz=640,conf=0.5)
results = model.predict(source=r'C:\Users\Zeeshan.khan\vscode_projects\checkout\Musk Melon_10-19-2022-16-16-5193205_Focus_48.png',save=True,imgsz=640,conf=0.5)
     

class_counts = {}  # Dictionary to store class counts

for result in results:
    boxes = result.boxes.cpu().numpy()  # Get boxes on CPU in numpy
    for box in boxes:
        class_index = int(box.cls[0])
        class_name = result.names[class_index]
        confidence = box.conf
        max_class = max(confidence)
        max_class = min(confidence)


        # Update class count
        if class_name in class_counts:
            class_counts[class_name] += 1
        else:
            class_counts[class_name] = 1

# Print the final class counts
for class_name, count in class_counts.items():
    print(f"{class_name}: {count}")


# class_counts = {}  # Dictionary to store class counts
# class_scores = {}  # Dictionary to store maximum and minimum scores

# for result in results:
#     boxes = result.boxes.cpu().numpy()  # Get boxes on CPU in numpy
#     for box in boxes:
#         class_index = int(box.cls[0])
#         class_name = result.names[class_index]
#         confidence = box.conf

#         # Update class count
#         if class_name in class_counts:
#             class_counts[class_name] += 1
#         else:
#             class_counts[class_name] = 1

#         # Update class scores
#         if class_name in class_scores:
#             max_confidence = max(class_scores[class_name]["max_confidence"], confidence)
#             min_confidence = min(class_scores[class_name]["min_confidence"], confidence)
#         else:
#             max_confidence = confidence
#             min_confidence = confidence

#         class_scores[class_name] = {
#             "max_confidence": max_confidence,
#             "min_confidence": min_confidence
#         }

# # Print the final class counts and confidence scores
# for class_name, count in class_counts.items():
#     print(f"{class_name}: {count}")
#     print(f"Max Confidence: {class_scores[class_name]['max_confidence']}")
#     print(f"Min Confidence: {class_scores[class_name]['min_confidence']}")








# import cv2
# import streamlit as st

# from PIL import Image
# from io import BytesIO
# from ultralytics import YOLO

# # Load the YOLO model
# model = YOLO('best.pt')

# def predict(image):
#     # Convert the image to OpenCV format
#     image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

#     # Pass the image through the YOLO model
#     results = model.predict(image, save=True, imgsz=640, conf=0.5)

#     # Get the result with bounding boxes plotted
#     res_plotted = results[0].plot()
    

#     # Convert the image back to PIL format for display
#     result_image = Image.fromarray(res_plotted)

#     return result_image


# def main():
#     st.title("Custom YOLO Segmentation App")

#     # File uploader
#     uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

#     if uploaded_file is not None:
#         # Read the uploaded image
#         image = Image.open(uploaded_file)

#         # Display the original image
#         st.subheader("Original Image")
#         st.image(image, use_column_width=True)

#         # Perform prediction and get the result image
#         result_image = predict(image)

#         # Display the segmented image
#         st.subheader("Segmented Image")
#         st.image(result_image, use_column_width=True)
        
# if __name__ == "__main__":
#     main()

