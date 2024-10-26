import cv2
import torch
import numpy as np
from ultralytics import YOLO  # Import the YOLO class from ultralytics package

# Load the YOLOv8 model directly using the Ultralytics library
model = YOLO(r'/Users/apple/Downloads/SIH-2 2/best-final-2.pt')

# Function to load and preprocess an image
def preprocess_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image, image_rgb

# Function to run the model and get predictions
def detect_sign_language(image_rgb):
    # Run inference using the YOLOv8 model
    results = model(image_rgb)
    return results[0]  # Extract the first result from the list

# Function to draw bounding boxes and labels on the image
def draw_bounding_boxes(image, result):
    # Access the bounding boxes from the result
    boxes = result.boxes  # Boxes object containing detection bounding boxes
    names = result.names  # Class names
    
    if boxes is not None:
        for box in boxes:
            # Extract bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Convert to integers
            # Extract label and confidence score
            label = names[int(box.cls[0])]  # Convert class ID to label name
            confidence = box.conf[0]  # Confidence score

            # Draw rectangle for bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Prepare the label text with confidence score
            label_text = f"{label} {confidence:.2f}"
            
            # Calculate the position to place the label
            (text_width, text_height), baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            label_y = max(y1, text_height + 10)  # Ensure the label is drawn above the box
            
            # Draw a filled rectangle for better text visibility
            cv2.rectangle(image, (x1, label_y - text_height - 10), (x1 + text_width, label_y + baseline - 10), (0, 255, 0), -1)
            # Put the label text on the bounding box
            cv2.putText(image, label_text, (x1, label_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    return image

# Main function to process an image
def process_image(image_path):
    # Load and preprocess the image
    image, image_rgb = preprocess_image(image_path)

    # Detect sign language in the image
    result = detect_sign_language(image_rgb)

    # Draw bounding boxes and labels
    output_image = draw_bounding_boxes(image, result)

    # Display the output image
    cv2.imshow('Sign Language Detection', output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the output image (optional)
    cv2.imwrite('output_image.jpg', output_image)

# Example usage
image_path = r'/Users/apple/Downloads/SIH-2 2/IMG-20240830-WA0006.jpg'
process_image(image_path)
