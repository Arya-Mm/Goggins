from ultralytics import YOLO


class YoloFloorPlanDetector:

    def __init__(self, model_path="core/models/best.pt"):
        self.model = YOLO(model_path)

    def detect(self, image):

        results = self.model(image)[0]

        detections = []

        for box in results.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({
                "class_id": cls,
                "confidence": conf,
                "bbox": [x1, y1, x2, y2]
            })

        return detections