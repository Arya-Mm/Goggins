import os
import time
from typing import Dict, List
import numpy as np
from ultralytics import YOLO


class StructuralDetector:
    """
    YOLO-based structural element detector.
    • Loads custom model if available
    • Falls back to yolov8n
    • Falls back to synthetic detection if inference fails
    """

    def __init__(
        self,
        model_path: str = None,
        confidence_threshold: float = 0.4
    ):
        self.conf_threshold = confidence_threshold
        self.model = None
        self.model_path = self._resolve_model_path(model_path)
        self.model_used = "none"
        self._load_model()

    # ─────────────────────────────────────────────────────────────
    # MODEL LOADING
    # ─────────────────────────────────────────────────────────────

    def _resolve_model_path(self, model_path: str) -> str:
        """
        Resolve absolute model path safely.
        """
        if model_path:
            return os.path.abspath(model_path)

        default_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "best.pt")
        )

        return default_path

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

    # ─────────────────────────────────────────────────────────────
    # DETECTION
    # ─────────────────────────────────────────────────────────────

    def detect(self, image: np.ndarray) -> Dict:
        """
        Run detection safely.

        Returns:
        {
            "elements": [...],
            "class_counts": {},
            "total_detections": int,
            "model_used": str,
            "inference_time_ms": float,
            "average_confidence": float
        }
        """

        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image provided to detector.")

        if self.model is None:
            return self._fallback_detection(image)

        try:
            start = time.time()
            results = self.model(image, verbose=False)[0]
            inference_time = (time.time() - start) * 1000

            if results.boxes is None:
                return self._fallback_detection(image)

            elements = []
            class_counts = {}
            confidences = []

            for box in results.boxes:
                conf = float(box.conf[0])

                if conf < self.conf_threshold:
                    continue

                cls_id = int(box.cls[0])
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                label = self.model.names.get(cls_id, "unknown")
                label = str(label).lower().strip().replace(" ", "_")

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

            if not elements:
                return self._fallback_detection(image)

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
            return self._fallback_detection(image)

    # ─────────────────────────────────────────────────────────────
    # FALLBACK
    # ─────────────────────────────────────────────────────────────

    def _fallback_detection(self, image: np.ndarray) -> Dict:
        """
        Minimal synthetic detection to keep pipeline alive.
        """

        h, w = image.shape[:2]

        synthetic = {
            "id": "synthetic_1",
            "type": "synthetic_column",
            "confidence": 0.5,
            "bbox": [
                int(w * 0.4),
                int(h * 0.4),
                int(w * 0.6),
                int(h * 0.6)
            ],
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