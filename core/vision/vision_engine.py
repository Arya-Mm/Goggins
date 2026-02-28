from pathlib import Path
from .dim_extractor.pdf_processor import PDFProcessor
from .yolo_adapter import YOLOAdapter
import fitz
import numpy as np


class VisionEngine:

    def __init__(self):
        self.processor = PDFProcessor()

        # Safe absolute model path
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
    # Normalize labels for Twin Layer
    # -----------------------------
    def _normalize_label(self, label):

        mapping = {
            "Wall": "walls",
            "Door": "doors",
            "Window": "windows",
            "Column": "columns",
            "Beam": "beams",
            "Slab": "slabs",
            "Dimension": "dimension_marks"
        }

        return mapping.get(label, label.lower())

    # -----------------------------
    # Structure & Filter Objects
    # -----------------------------
    def _structure_objects(self, detections, min_conf=0.4):
        structured = {}

        for obj in detections:
            if obj["confidence"] < min_conf:
                continue

            norm_label = self._normalize_label(obj["label"])
            structured.setdefault(norm_label, []).append(obj)

        return structured

    # -----------------------------
    # MAIN ENTRY
    # -----------------------------
    def run(self, pdf_path):

        # 1️⃣ Dimension Extraction
        data = self.processor.extract_with_pymupdf(pdf_path)

        dimensions = []
        for page in data.get("pages", []):
            dimensions.extend(page.get("dimensions", []))

        # 2️⃣ YOLO Detection
        image = self._pdf_to_image(pdf_path)
        raw_objects = self.yolo.detect(image)

        # 3️⃣ Structure Objects
        structured_objects = self._structure_objects(raw_objects)

        return {
            "dimensions": dimensions,
            "objects": structured_objects
        }