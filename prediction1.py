import cv2
import streamlit as st

from PIL import Image
from io import BytesIO
from ultralytics import YOLO
import numpy as np

# Load the YOLO model
model = YOLO('last.pt')

def predict1(image):
    # Convert the image to OpenCV format
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Pass the image through the YOLO model
    results = model.predict(image, save=True, imgsz=640, conf=0.5)

    # Get the result with bounding boxes plotted
    res_plotted = results[0].plot()

    # Convert the image back to PIL format for display
    result_image = Image.fromarray(res_plotted)

    return result_image

def predict2(image):
    # Convert the image to OpenCV format
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Pass the image through the YOLO model
    results1 = model.predict(image, save=True, imgsz=640, conf=0.5)

    return results1


def main():
    st.title("Custom YOLO Segmentation App")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the uploaded image
        image = Image.open(uploaded_file)

        # Display the original image
        st.subheader("Original Image")
        st.image(image, use_column_width=True)

        # Perform prediction and get the result image
        result_image = predict1(image)

        # Display the segmented image
        st.subheader("Segmented Image")
        st.image(result_image, use_column_width=True)

        results3 = predict2(image)
        class_counts = {}  # Dictionary to store class counts
        class_scores = {}  # Dictionary to store maximum and minimum scores
        class_names = []
        for result in results3:
            boxes = result.boxes.cpu().numpy()  # Get boxes on CPU in numpy
            for box in boxes:
                class_index = int(box.cls[0])
                class_name = result.names[class_index]
                confidence = box.conf

                # Update class count
                if class_name in class_counts:
                    class_counts[class_name] += 1
                else:
                    class_counts[class_name] = 1

                # Update class scores
                if class_name in class_scores:
                    max_confidence = max(class_scores[class_name]["max_confidence"], confidence)
                    min_confidence = min(class_scores[class_name]["min_confidence"], confidence)
                else:
                    max_confidence = confidence
                    min_confidence = confidence

                class_scores[class_name] = {
                    "max_confidence": max_confidence,
                    "min_confidence": min_confidence
                }
                class_names.append(class_name)


                # Check if more than one class is detected
        if len(set(class_names)) > 1:
            class_counts = {"Mixed Fruit": len(class_names)}
            class_scores = {}

        # Save the segmented image
        result_image_path = "segmented_image.png"
        result_image.save(result_image_path)


        # Print the final class counts and confidence scores
        for class_name, count in class_counts.items():
            # st.write(f"{class_name}: {count}")
            st.write(f"Detection : {class_name}")
            if class_name != "Mixed Fruit":
                st.write(f"Max Confidence: {class_scores[class_name]['max_confidence']}")
                # st.write(f"Min Confidence: {class_scores[class_name]['min_confidence']}")

if __name__ == "__main__":
    main()


