import cv2
import easyocr
import threading
from queue import Queue
from time import time
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# -----------------------------
# CPU Optimized OCR Initialization
# -----------------------------
reader = easyocr.Reader(['en'], gpu=False,  # Force CPU
                       model_storage_directory='./models',
                       download_enabled=True,
                       detector=True,
                       recognizer=True,
                       verbose=False)

# -----------------------------
# Threaded OCR Detector
# -----------------------------
class OCRThread:
    def __init__(self):
        self.frame_queue = Queue(maxsize=1)
        self.result_queue = Queue(maxsize=1)
        self.latest_results = []
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        self.frame_counter = 0

    def run(self):
        while True:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                self.latest_results = self.detect_text(frame)
                if self.result_queue.full():
                    try: self.result_queue.get_nowait()
                    except: pass
                self.result_queue.put(self.latest_results)

    def detect_text(self, frame, min_confidence=0.6):
        # Downscale frame for speed
        h, w = frame.shape[:2]
        scale = min(640 / w, 480 / h)
        if scale < 1:
            frame = cv2.resize(frame, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        processed = cv2.GaussianBlur(gray, (3,3), 0)
        processed = cv2.convertScaleAbs(processed, alpha=1.2, beta=10)
        
        results = reader.readtext(
            processed,
            paragraph=False,
            width_ths=0.8,
            height_ths=0.8,
            min_size=30,
            text_threshold=0.7,
            low_text=0.5,
            link_threshold=0.5,
            canvas_size=960,
            mag_ratio=0.8
        )
        
        detections = []
        for bbox, text, prob in results:
            if prob > min_confidence and len(text.strip()) > 2:
                if scale < 1:
                    bbox = np.array(bbox)/scale
                bbox = np.array(bbox).astype(int)
                detections.append((bbox, text, prob))
        return detections

    def add_frame(self, frame):
        self.frame_counter += 1
        # Submit every 30 frames for CPU
        if self.frame_counter >= 30:
            if self.frame_queue.full():
                try: self.frame_queue.get_nowait()
                except: pass
            self.frame_queue.put(frame)
            self.frame_counter = 0

    def get_results(self):
        if not self.result_queue.empty():
            try: self.latest_results = self.result_queue.get_nowait()
            except: pass
        return self.latest_results

# -----------------------------
# Initialize OCR thread
# -----------------------------
ocr_detector = OCRThread()

# -----------------------------
# Video Capture
# -----------------------------
cap = cv2.VideoCapture(0)  # Webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 15)

cv2.namedWindow("Text Detection", cv2.WINDOW_NORMAL)

fps_start = time()
fps = 0
frame_count = 0

print("Text detection ready. Press 'q' to quit, 's' to save screenshot.")

# -----------------------------
# Main Loop
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    current_time = time()
    if frame_count >= 15:
        fps = 15 / (current_time - fps_start)
        fps_start = current_time
        frame_count = 0

    annotated = frame.copy()

    # Submit frame to OCR
    ocr_detector.add_frame(frame)
    ocr_results = ocr_detector.get_results()

    # Draw OCR boxes
    for bbox, text, _ in ocr_results:
        x1, y1 = bbox[0]
        x2, y2 = bbox[2]
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (255,100,0), 2)
        cv2.putText(annotated, text[:20], (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)

    # Draw FPS
    cv2.rectangle(annotated, (5,5), (120,50), (0,0,0), -1)
    cv2.putText(annotated, f"FPS: {fps:.1f}", (10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0),1)
    status_text = "OCR" if ocr_detector.frame_queue.qsize()>0 else "Ready"
    cv2.putText(annotated, status_text, (10,45), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,0),1)

    cv2.imshow("Text Detection", annotated)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite(f"screenshot_{int(time())}.jpg", annotated)
        print("Screenshot saved!")

cap.release()
cv2.destroyAllWindows()
