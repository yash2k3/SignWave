import cv2
import time
from ultralytics import YOLO

# Load the pre-trained YOLO model
model = YOLO(r"/Users/apple/Desktop/SignWave/best-final-2.pt")  # Replace with the path to your model

# Define the hand sign labels that the model can detect
labels = ["Hello", "Help", "Home", "No", "Please", "Yes"]

# Initialize variables for detection timing
detected_start_time = None
min_detection_duration = 3  # Minimum duration for detection in seconds
detected_label = None
detection_paused = False  # To handle detection pausing

# Predict with showing the images (adjusted to display bounding boxes)
results = model.predict(source="0", show=True, conf=0.3)  # Use source=0 for webcam input

while True:
    for result in results:
        # Get the original image
        img = result.orig_img
        current_time = time.time()
        detected_this_frame = False

        # Loop through the detections in the current frame
        for det in result.boxes.data:
            # Get the label and confidence score for the detected object
            class_id = int(det.cls[0])
            label = labels[class_id]  # Get the label from the predefined list
            confidence = det.conf[0]

            # Check if the detected object is one of the specified hand signs
            if label in labels:
                detected_this_frame = True

                # Check if we are currently pausing detection
                if detection_paused:
                    continue

                if detected_start_time is None:
                    detected_start_time = current_time
                    detected_label = label

                # Extract bounding box coordinates (x1, y1, x2, y2)
                x1, y1, x2, y2 = map(int, det.xyxy[0])

                # Draw the bounding box
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box with thickness 2

                # Put the label and confidence on the bounding box
                cv2.putText(img, f"{label} {confidence:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Green text with thickness 2

                # Once an object is detected, pause further detections
                detection_paused = True

        # Check if a hand sign has been detected continuously for the required duration
        if detected_this_frame and detection_paused:
            if detected_start_time and (current_time - detected_start_time) >= min_detection_duration:
                print(f"Detected {detected_label} continuously for {min_detection_duration} seconds")
                # Store or process detected data here if needed
                detected_start_time = None  # Reset detection start time after storing data
                detection_paused = False  # Resume detection after processing
        else:
            detected_start_time = None  # Reset detection start time if no detection in this frame
            detection_paused = False  # Resume detection if nothing is detected

        # Display the image with bounding boxes
        cv2.imshow("Hand Sign Detection", img)

        # Introduce a delay to make the detection smooth and slow
        cv2.waitKey(500)  # 500 ms delay

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Break out of the outer loop to stop the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
