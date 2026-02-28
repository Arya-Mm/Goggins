from ultralytics import YOLO
import numpy as np


class YOLOAdapter:

    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def detect(self, image: np.ndarray):

        results = self.model(image)[0]

        detections = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = self.model.names[cls_id]
            conf = float(box.conf[0])
            coords = box.xyxy[0].tolist()

            detections.append({
                "label": label,
                "confidence": round(conf, 3),
                "bbox": coords
            })

        return detections