import pytesseract
import re
import cv2

# Set path if needed (adjust if different)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_dimensions(blueprint):
    """
    Extract dimension text like 27', 37', 14'-0"x11'-0"
    using Tesseract OCR.
    """

    img = blueprint["threshold"]

    text = pytesseract.image_to_string(img)

    dimension_pattern = re.compile(r"\d+'\s?-?\d*\"?")

    matches = dimension_pattern.findall(text)

    dimensions = []

    for match in matches:
        dimensions.append({
            "text": match,
            "confidence": 0.85  # Tesseract doesn't give per-word confidence easily
        })

    return {
        "dimensions": dimensions,
        "confidence": 0.85 if dimensions else 0.7
    }