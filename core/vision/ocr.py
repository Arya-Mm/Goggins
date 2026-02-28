from paddleocr import PaddleOCR
import re

# Initialize OCR once
ocr_model = PaddleOCR(use_angle_cls=True, lang='en')


def extract_dimensions(blueprint):
    """
    Extract dimension text like 27', 37', 14'-0"x11'-0"
    """

    img = blueprint["original_image"]

    results = ocr_model.ocr(img, cls=True)

    dimensions = []
    total_conf = 0
    count = 0

    dimension_pattern = re.compile(r"\d+'\s?-?\d*\"?")

    for line in results:
        for word_info in line:
            text = word_info[1][0]
            conf = word_info[1][1]

            if dimension_pattern.search(text):
                dimensions.append({
                    "text": text,
                    "confidence": float(conf)
                })
                total_conf += conf
                count += 1

    avg_conf = total_conf / count if count > 0 else 0.8

    return {
        "dimensions": dimensions,
        "confidence": round(avg_conf, 3)
    }