from ultralytics import YOLO
import cv2

class StructuralDetector:
    def __init__(self):
        # Using yolov8n (nano) for speed and CPU efficiency
        # In a real hackathon, you'd point this to your trained .pt file
        self.model = YOLO('yolov8n.pt') 
        self.confidence_threshold = 0.45

    def analyze(self, raw_data):
        img = raw_data["original"]
        results = self.model(img)[0]
        
        detections = []
        for box in results.boxes:
            conf = float(box.conf[0])
            if conf > self.confidence_threshold:
                cls = int(box.cls[0])
                name = results.names[cls]
                coords = box.xyxy[0].tolist() # [x1, y1, x2, y2]
                
                detections.append({
                    "type": name,
                    "bbox": coords,
                    "confidence": conf
                })
        
        return detections