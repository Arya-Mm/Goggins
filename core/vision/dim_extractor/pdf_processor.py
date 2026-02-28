import pdfplumber
import fitz
from typing import Dict
from .dimension_parser import DimensionParser


class PDFProcessor:
    def __init__(self):
        self.dimension_parser = DimensionParser()

    # ==============================
    # PRIMARY METHOD (PyMuPDF)
    # ==============================
    def extract_with_pymupdf(self, pdf_path: str) -> Dict:
        results = {"pages": []}

        try:
            doc = fitz.open(pdf_path)

            for page_num in range(len(doc)):
                page = doc[page_num]
                page_data = self._process_page_pymupdf(page, page_num + 1)
                results["pages"].append(page_data)

            doc.close()
            return results

        except Exception as e:
            print(f"[PDFProcessor] PyMuPDF error: {e}")
            return results

    def _process_page_pymupdf(self, page, page_num: int) -> Dict:
        dimensions = []

        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        bbox = span["bbox"]

                        dims = self.dimension_parser.extract_dimensions_from_text(
                            text, bbox
                        )
                        dimensions.extend(dims)

        return {
            "page": page_num,
            "dimensions": dimensions,
            "codes": []
        }

    # ==============================
    # BACKUP METHOD (pdfplumber)
    # ==============================
    def extract_with_pdfplumber(self, pdf_path: str) -> Dict:
        results = {"pages": []}

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_data = self._process_page_plumber(page, page_num)
                    results["pages"].append(page_data)

            return results

        except Exception as e:
            print(f"[PDFProcessor] pdfplumber error: {e}")
            return results

    def _process_page_plumber(self, page, page_num: int) -> Dict:
        dimensions = []

        words = page.extract_words()

        for word in words:
            text = word["text"]
            bbox = [word["x0"], word["top"], word["x1"], word["bottom"]]

            dims = self.dimension_parser.extract_dimensions_from_text(
                text, bbox
            )
            dimensions.extend(dims)

        return {
            "page": page_num,
            "dimensions": dimensions,
            "codes": []
        }