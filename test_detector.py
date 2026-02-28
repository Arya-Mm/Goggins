import cv2
from core.vision.detector import StructuralDetector

img = cv2.imread("test_blueprint.png")

detector = StructuralDetector()
result = detector.detect(img)

print("Total detections:", result["total_detections"])
print("Classes:", result["class_counts"])
print("Model:", result["model_used"])