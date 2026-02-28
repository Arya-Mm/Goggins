from ultralytics import YOLO


class YoloPerception:

    def __init__(self, model_path="core/models/best.pt"):
        self.model = YOLO(model_path)

    def detect(self, image_path):

        results = self.model(image_path)[0]

        detections = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({
                "class_id": cls_id,
                "confidence": conf,
                "bbox": [x1, y1, x2, y2]
            })

        return detections