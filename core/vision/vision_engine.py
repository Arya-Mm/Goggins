# core/vision/vision_engine.py

from pathlib import Path
from .dim_extractor.pdf_processor import PDFProcessor
from .yolo_adapter import YOLOAdapter
import fitz
import numpy as np


class VisionEngine:

    def __init__(self):
        self.processor = PDFProcessor()

        base_dir = Path(__file__).resolve().parents[2]
        model_path = base_dir / "core" / "data" / "best.pt"

        self.yolo = YOLOAdapter(str(model_path))

    # -----------------------------
    # Convert PDF → Image
    # -----------------------------
    def _pdf_to_image(self, pdf_path):
        doc = fitz.open(pdf_path)
        page = doc[0]
        pix = page.get_pixmap()
        doc.close()

        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, pix.n
        )

        return img

    # -----------------------------
    # Robust Label Normalization (FIXED)
    # -----------------------------
    def _normalize_label(self, label):

        label = str(label).lower().strip().replace(" ", "_")

        mapping = {
            "wall": "walls",
            "walls": "walls",

            "door": "doors",
            "sliding_door": "doors",
            "doors": "doors",

            "window": "windows",
            "windows": "windows",

            "column": "columns",
            "columns": "columns",

            "beam": "beams",
            "beams": "beams",

            "slab": "slabs",
            "slabs": "slabs"
        }

        return mapping.get(label, None)

    # -----------------------------
    # Structure & Filter Objects (FIXED)
    # -----------------------------
    def _structure_objects(self, detections, min_conf=0.4):

        structured = {
            "walls": [],
            "doors": [],
            "windows": [],
            "columns": [],
            "beams": [],
            "slabs": []
        }

        for obj in detections:

            if obj["confidence"] < min_conf:
                continue

            norm_label = self._normalize_label(obj["label"])

            if norm_label:
                structured[norm_label].append(obj)

        return structured

    # -----------------------------
    # MAIN ENTRY
    # -----------------------------
    def run(self, pdf_path):

        # 1️⃣ Extract Dimensions
        data = self.processor.extract_with_pymupdf(pdf_path)

        dimensions = []
        for page in data.get("pages", []):
            dimensions.extend(page.get("dimensions", []))

        # 2️⃣ YOLO Detection
        image = self._pdf_to_image(pdf_path)
        raw_detections = self.yolo.detect(image)

        # 3️⃣ Structure Objects
        structured_objects = self._structure_objects(raw_detections)

        return {
            "dimensions": dimensions,
            "objects": structured_objects
        }