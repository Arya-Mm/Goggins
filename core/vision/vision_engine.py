from .dim_extractor.pdf_processor import PDFProcessor


class VisionEngine:

    def __init__(self):
        self.processor = PDFProcessor()

    def run(self, pdf_path):

        data = self.processor.extract_with_pymupdf(pdf_path)

        dimensions = []
        for page in data.get("pages", []):
            dimensions.extend(page.get("dimensions", []))

        return {
            "dimensions": dimensions
        }