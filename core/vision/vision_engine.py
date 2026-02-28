from .dim_extractor.pdf_processor import process_pdf
from .dim_extractor.dimension_parser import parse_dimensions
from .yolo_detector import YOLODetector
import fitz
import numpy as np


class VisionEngine:

    def __init__(self):
        self.yolo = YOLODetector("core/models/best.pt")

    def pdf_to_image(self, pdf_path):
        doc = fitz.open(pdf_path)
        page = doc[0]
        pix = page.get_pixmap()
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, pix.n
        )
        return img

    def run(self, pdf_path):

        # 1️⃣ Extract dimensions
        pdf_data = process_pdf(pdf_path)
        dimensions = parse_dimensions(pdf_data)

        # 2️⃣ Convert to image
        image = self.pdf_to_image(pdf_path)

        # 3️⃣ Run YOLO
        objects = self.yolo.detect(image)

        return {
            "dimensions": dimensions,
            "objects": objects
        }