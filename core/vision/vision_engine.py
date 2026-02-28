from pathlib import Path
from .dim_extractor.pdf_processor import PDFProcessor
from .yolo_adapter import YOLOAdapter
import fitz
import numpy as np


class VisionEngine:

    def __init__(self):
        self.processor = PDFProcessor()

        # Absolute safe model path
        base_dir = Path(__file__).resolve().parents[2]
        model_path = base_dir / "core" / "data" / "best.pt"

        self.yolo = YOLOAdapter(str(model_path))

    def _pdf_to_image(self, pdf_path):
        doc = fitz.open(pdf_path)
        page = doc[0]
        pix = page.get_pixmap()
        doc.close()

        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, pix.n
        )

        return img

    def _structure_objects(self, detections, min_conf=0.4):
        structured = {}

        for obj in detections:
            if obj["confidence"] < min_conf:
                continue

            label = obj["label"]
            structured.setdefault(label, []).append(obj)

        return structured

    def run(self, pdf_path):

        # 1️⃣ Dimension Extraction
        data = self.processor.extract_with_pymupdf(pdf_path)

        dimensions = []
        for page in data.get("pages", []):
            dimensions.extend(page.get("dimensions", []))

        # 2️⃣ YOLO Detection
        image = self._pdf_to_image(pdf_path)
        raw_objects = self.yolo.detect(image)

        # 3️⃣ Structure & Filter Objects
        structured_objects = self._structure_objects(raw_objects)

        return {
            "dimensions": dimensions,
            "objects": structured_objects
        }