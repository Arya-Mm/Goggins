from ultralytics import YOLO
import numpy as np

# Load model once (global)
model = YOLO("yolov8n.pt")


def detect_structural_elements(blueprint):
    """
    Runs YOLO detection and maps detections
    into structural primitives.
    """

    img = blueprint["original_image"]

    results = model(img, verbose=False)

    columns = []
    beams = []
    slabs = []

    total_confidence = 0
    count = 0

    for r in results:
        boxes = r.boxes
        if boxes is None:
            continue

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = float(box.conf[0].cpu().numpy())

            width = x2 - x1
            height = y2 - y1

            aspect_ratio = width / height if height != 0 else 0

            element = {
                "bbox": [float(x1), float(y1), float(x2), float(y2)],
                "confidence": conf
            }

            # Heuristic mapping
            if 0.8 < aspect_ratio < 1.2:
                columns.append(element)
            elif aspect_ratio > 2:
                beams.append(element)
            else:
                slabs.append(element)

            total_confidence += conf
            count += 1

    avg_confidence = total_confidence / count if count > 0 else 0.8

    return {
        "columns": columns,
        "beams": beams,
        "slabs": slabs,
        "confidence": round(avg_confidence, 3)
    }