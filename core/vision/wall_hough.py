import cv2
import numpy as np


def detect_walls(blueprint):
    """
    Detect walls using Hough Line Transform.
    Uses precomputed edges from ingestion layer.
    """

    edges = blueprint["edges"]

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=120,
        minLineLength=100,
        maxLineGap=10
    )

    walls = []

    if lines is None:
        return walls

    for line in lines:
        x1, y1, x2, y2 = line[0]

        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # Filter small lines
        if length < 150:
            continue

        orientation = "horizontal" if abs(y2 - y1) < abs(x2 - x1) else "vertical"

        walls.append({
            "start": [int(x1), int(y1)],
            "end": [int(x2), int(y2)],
            "length_pixels": round(float(length), 2),
            "orientation": orientation,
            "confidence": 0.85
        })

    return walls