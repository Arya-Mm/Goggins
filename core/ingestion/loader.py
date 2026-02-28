import cv2
import os
import numpy as np
from typing import Dict


class BlueprintLoader:
    """
    Loads and preprocesses blueprint images.
    """

    def __init__(self):
        pass

    def load(self, image_path: str) -> Dict:
        """
        Load and preprocess blueprint.

        Returns:
            {
                "original": image,
                "gray": gray_image,
                "threshold": thresh_image,
                "edges": edge_image,
                "width": int,
                "height": int,
                "success": bool
            }
        """

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Blueprint not found: {image_path}")

        image = cv2.imread(image_path)

        if image is None:
            raise ValueError("Failed to load image. Unsupported format.")

        height, width = image.shape[:2]

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Adaptive threshold (good for blueprints)
        thresh = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2
        )

        # Edge detection
        edges = cv2.Canny(gray, 50, 150)

        return {
            "original": image,
            "gray": gray,
            "threshold": thresh,
            "edges": edges,
            "width": width,
            "height": height,
            "success": True
        }