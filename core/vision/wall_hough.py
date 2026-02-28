import cv2
import numpy as np


def detect_walls(blueprint):
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

        orientation = "horizontal" if abs(y2 - y1) < abs(x2 - x1) else "vertical"

        walls.append({
            "start": [int(x1), int(y1)],
            "end": [int(x2), int(y2)],
            "length_pixels": float(length),
            "orientation": orientation,
            "confidence": 0.85
        })

    # Sort by length descending
    walls = sorted(walls, key=lambda w: w["length_pixels"], reverse=True)

    return walls