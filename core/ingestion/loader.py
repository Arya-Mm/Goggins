import cv2
import numpy as np
import tempfile
import os
from PIL import Image
import fitz  # PyMuPDF


def load_blueprint(uploaded_file):
    """
    Loads blueprint from image or PDF and applies preprocessing.
    Returns dictionary with:
        - original_image
        - grayscale
        - threshold
        - edges
        - metadata
    """

    if uploaded_file is None:
        raise ValueError("No file uploaded")

    filename = uploaded_file.name
    file_extension = filename.split(".")[-1].lower()

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix="." + file_extension) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    # =============================
    # HANDLE PDF
    # =============================
    if file_extension == "pdf":
        doc = fitz.open(temp_path)
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=200)
        img = np.frombuffer(pix.samples, dtype=np.uint8)
        img = img.reshape(pix.height, pix.width, pix.n)
        if pix.n == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        doc.close()

    # =============================
    # HANDLE IMAGE
    # =============================
    else:
        image = Image.open(temp_path).convert("RGB")
        img = np.array(image)

    os.remove(temp_path)

    # =============================
    # PREPROCESSING
    # =============================

    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    threshold = cv2.adaptiveThreshold(
        grayscale,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    edges = cv2.Canny(grayscale, 50, 150)

    return {
        "original_image": img,
        "grayscale": grayscale,
        "threshold": threshold,
        "edges": edges,
        "metadata": {
            "filename": filename,
            "file_type": file_extension,
            "resolution": img.shape
        }
    }
    