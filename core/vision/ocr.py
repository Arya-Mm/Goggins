import pytesseract
import re
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_dimensions(blueprint):
    """
    Geometry-guided OCR using longest boundary lines.
    """

    img = blueprint["grayscale"]
    walls = blueprint.get("walls", [])

    dimensions = []

    if not walls:
        return {"dimensions": [], "confidence": 0.7}

    # Find longest horizontal and vertical walls
    horizontal = next((w for w in walls if w["orientation"] == "horizontal"), None)
    vertical = next((w for w in walls if w["orientation"] == "vertical"), None)

    h, w = img.shape

    combined_text = ""

    # ---- Horizontal band OCR ----
    if horizontal:
        y = horizontal["start"][1]
        band = img[max(y - 40, 0):min(y + 40, h), :]
        text = pytesseract.image_to_string(band, config="--psm 6")
        combined_text += text + " "

    # ---- Vertical band OCR ----
    if vertical:
        x = vertical["start"][0]
        band = img[:, max(x - 40, 0):min(x + 40, w)]
        text = pytesseract.image_to_string(band, config="--psm 6")
        combined_text += text

    # Extract dimensions
    pattern = re.compile(r"\d+'\s?-?\d*\"?")
    matches = pattern.findall(combined_text)

    for m in matches:
        dimensions.append({
            "text": m.strip(),
            "confidence": 0.92
        })

    return {
        "dimensions": dimensions,
        "confidence": 0.92 if dimensions else 0.7
    }