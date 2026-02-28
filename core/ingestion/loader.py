import cv2
import numpy as np
import os

class DrawingLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        """Loads image and applies initial normalization."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Drawing not found at {self.file_path}")
        
        # Load image
        img = cv2.imread(self.file_path)
        
        # Preprocessing: Grayscale & Denoising
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        normalized = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Adaptive Thresholding for line enhancement
        thresh = cv2.adaptiveThreshold(
            normalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )

        return {
            "original": img,
            "processed": thresh,
            "metadata": {
                "filename": os.path.basename(self.file_path),
                "dimensions": img.shape[:2]
            }
        }