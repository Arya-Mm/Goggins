import os
import time
from typing import Dict
import numpy as np
from ultralytics import YOLO


class StructuralDetector:
    """
    YOLO-based structural element detector.
    Stable hybrid detection layer.
    """

    def __init__(
        self,
        model_path: str = None,
        confidence_threshold: float = 0.25
    ):
        self.conf_threshold = confidence_threshold
        self.model = None
        self.model_used = "none"
        self.model_path = self._resolve_model_path(model_path)

        self.allowed_classes = {
            "column",
            "wall",
            "curtain_wall",
            "stair_case",
            "door",
            "sliding_door",
            "window",
            "railing"
        }

        self._load_model()

    # ─────────────────────────────────────────────
    # MODEL LOADING
    # ─────────────────────────────────────────────

    def _resolve_model_path(self, model_path: str):
        if model_path:
            return os.path.abspath(model_path)

        return os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "best.pt")
        )

    def _load_model(self):
        try:
            if os.path.exists(self.model_path):
                self.model = YOLO(self.model_path)
                self.model_used = os.path.basename(self.model_path)
                print(f"[YOLO] Loaded custom model: {self.model_used}")
            else:
                self.model = YOLO("yolov8n.pt")
                self.model_used = "yolov8n.pt"
                print("[YOLO] Loaded fallback yolov8n.pt")

        except Exception as e:
            print(f"[YOLO] Model load failed: {e}")
            self.model = None
            self.model_used = "none"

    # ─────────────────────────────────────────────
    # DETECTION
    # ─────────────────────────────────────────────

    def detect(self, image: np.ndarray) -> Dict:

        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image provided to detector.")

        if self.model is None:
            return self._synthetic_detection(image)

        try:
            start = time.time()
            results = self.model(image, verbose=False)[0]
            inference_time = (time.time() - start) * 1000

            if results.boxes is None:
                print("[YOLO] No detections at all.")
                return self._empty_detection(inference_time)

            elements = []
            class_counts = {}
            confidences = []

            raw_count = len(results.boxes)

            for box in results.boxes:
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                label = self.model.names.get(cls_id, "unknown")
                label = str(label).lower().strip().replace(" ", "_")

                # ignore dimension class
                if label == "dimension":
                    continue

                if label not in self.allowed_classes:
                    continue

                if conf < self.conf_threshold:
                    continue

                class_counts[label] = class_counts.get(label, 0) + 1
                confidences.append(conf)

                elements.append({
                    "id": f"{label}_{len(elements)+1}",
                    "type": label,
                    "confidence": round(conf, 4),
                    "bbox": [
                        int(max(0, x1)),
                        int(max(0, y1)),
                        int(max(0, x2)),
                        int(max(0, y2))
                    ],
                    "synthetic": False
                })

            print(f"[YOLO] Raw detections: {raw_count}")
            print(f"[YOLO] After filtering: {len(elements)}")

            if not elements:
                return self._empty_detection(inference_time)

            avg_conf = sum(confidences) / len(confidences)

            return {
                "elements": elements,
                "class_counts": class_counts,
                "total_detections": len(elements),
                "model_used": self.model_used,
                "inference_time_ms": round(inference_time, 2),
                "average_confidence": round(avg_conf, 4)
            }

        except Exception as e:
            print(f"[YOLO] Detection failed: {e}")
            return self._synthetic_detection(image)

    # ─────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────

    def _empty_detection(self, inference_time):
        return {
            "elements": [],
            "class_counts": {},
            "total_detections": 0,
            "model_used": self.model_used,
            "inference_time_ms": round(inference_time, 2),
            "average_confidence": 0.0
        }

    def _synthetic_detection(self, image):
        h, w = image.shape[:2]
        synthetic = {
            "id": "synthetic_1",
            "type": "synthetic_column",
            "confidence": 0.5,
            "bbox": [int(w * 0.4), int(h * 0.4), int(w * 0.6), int(h * 0.6)],
            "synthetic": True
        }
        return {
            "elements": [synthetic],
            "class_counts": {"synthetic_column": 1},
            "total_detections": 1,
            "model_used": "fallback_synthetic",
            "inference_time_ms": 0.0,
            "average_confidence": 0.5
        }