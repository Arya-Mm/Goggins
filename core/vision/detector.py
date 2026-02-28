import os
from typing import Dict, List
from ultralytics import YOLO
import numpy as np


class StructuralDetector:
    """
    YOLO-based structural element detector.
    Safe fallback if model fails.
    """

    def __init__(self, model_path: str = "core/data/best.pt"):
        self.model = None
        self.model_path = model_path
        self._load_model()

    def _load_model(self):
        try:
            if self.model_path and os.path.exists(self.model_path):
                self.model = YOLO(self.model_path)
                print(f"[YOLO] Loaded custom model: {self.model_path}")
            else:
                self.model = YOLO("yolov8n.pt")
                print("[YOLO] Loaded default yolov8n.pt")
        except Exception as e:
            print(f"[YOLO] Model load failed: {e}")
            self.model = None

    def detect(self, image: np.ndarray) -> Dict:
        """
        Run YOLO detection.

        Returns:
            {
                "elements": [...],
                "class_counts": {},
                "total_detections": int,
                "model_used": str
            }
        """

        if self.model is None:
            return self._fallback_detection(image)

        try:
            results = self.model(image, verbose=False)[0]
            boxes = results.boxes

            elements = []
            class_counts = {}

            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                label = self.model.names.get(cls_id, "unknown")

                class_counts[label] = class_counts.get(label, 0) + 1

                elements.append({
                    "type": label,
                    "confidence": round(conf, 4),
                    "bbox": [int(x1), int(y1), int(x2), int(y2)],
                    "synthetic": False
                })

            if len(elements) == 0:
                return self._fallback_detection(image)

            return {
                "elements": elements,
                "class_counts": class_counts,
                "total_detections": len(elements),
                "model_used": str(self.model_path or "yolov8n.pt")
            }

        except Exception as e:
            print(f"[YOLO] Detection failed: {e}")
            return self._fallback_detection(image)

    def _fallback_detection(self, image: np.ndarray) -> Dict:
        """
        Create minimal synthetic detection so pipeline never breaks.
        """

        h, w = image.shape[:2]

        synthetic_element = {
            "type": "synthetic_column",
            "confidence": 0.5,
            "bbox": [int(w*0.4), int(h*0.4), int(w*0.6), int(h*0.6)],
            "synthetic": True
        }

        return {
            "elements": [synthetic_element],
            "class_counts": {"synthetic_column": 1},
            "total_detections": 1,
            "model_used": "fallback_synthetic"
        }