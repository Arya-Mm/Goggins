import pytesseract
import re
import cv2

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_dimensions(blueprint):
    """
    Extract dimension text like 27', 37', 14'-0"x11'-0"
    using Tesseract OCR on grayscale image.
    """

    img = blueprint["grayscale"]

    # Improve OCR clarity
    img = cv2.GaussianBlur(img, (3, 3), 0)

    text = pytesseract.image_to_string(img, config="--psm 6")

    # Improved regex for architectural dimensions
    dimension_pattern = re.compile(r"\d+'\s?-?\d*\"?")

    matches = dimension_pattern.findall(text)

    dimensions = []

    for match in matches:
        dimensions.append({
            "text": match.strip(),
            "confidence": 0.85
        })

    return {
        "dimensions": dimensions,
        "confidence": 0.85 if dimensions else 0.7
    }