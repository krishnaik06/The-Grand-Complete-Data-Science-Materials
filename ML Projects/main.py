from ultralytics import YOLO
import cv2
import torch
from time import time

# Auto-select device (GPU if available, else CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load YOLOv8n model (faster for real-time)
model = YOLO("yolov8n.pt")

# Open webcam (0 is usually the default webcam)
cap = cv2.VideoCapture(0)

# Set webcam properties for better performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

# Create window
cv2.namedWindow("Live Detection", cv2.WINDOW_NORMAL)

# Class names from COCO dataset
class_names = model.names

# Initialize FPS counter
fps_start_time = time()
fps = 0
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Update FPS counter
    frame_count += 1
    if frame_count >= 30:
        fps = 30 / (time() - fps_start_time)
        fps_start_time = time()
        frame_count = 0

    # Run inference with adjusted confidence threshold for real-time
    results = model(frame, conf=0.3, iou=0.45)[0]

    # Initialize counters
    counts = {name: 0 for name in class_names.values()}

    # Process detections
    annotated_frame = frame.copy()
    
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        cls = int(box.cls[0])
        
        counts[class_names[cls]] += 1
        
        # Draw bounding box
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Add label
        label = f"{class_names[cls]}: {confidence:.2f}"
        cv2.putText(annotated_frame, label, (x1, y1-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display counts and FPS
    counts_text = " | ".join([f"{name}: {count}" for name, count in counts.items() if count > 0])
    fps_text = f"FPS: {fps:.1f}"
    
    cv2.putText(annotated_frame, counts_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(annotated_frame, fps_text, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show frame
    cv2.imshow("Live Detection", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()