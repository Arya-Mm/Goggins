from .dim_extractor.pdf_processor import PDFProcessor
from .yolo_adapter import YOLOAdapter
import fitz
import numpy as np


class VisionEngine:

    def __init__(self):
        self.processor = PDFProcessor()
        self.yolo = YOLOAdapter("core/data/best.pt")

    def _pdf_to_image(self, pdf_path):

        doc = fitz.open(pdf_path)
        page = doc[0]
        pix = page.get_pixmap()
        doc.close()

        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, pix.n
        )

        return img

    def run(self, pdf_path):

        # 1️⃣ Dimension Extraction
        data = self.processor.extract_with_pymupdf(pdf_path)

        dimensions = []
        for page in data.get("pages", []):
            dimensions.extend(page.get("dimensions", []))

        # 2️⃣ YOLO Structural Detection
        image = self._pdf_to_image(pdf_path)
        objects = self.yolo.detect(image)

        return {
            "dimensions": dimensions,
            "objects": objects
        }