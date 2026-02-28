# core/vision/scale_calibration.py

def calibrate_scale(detected_dimensions):
    """
    Explicit scale calibration logic.
    Converts pixel length to real-world units.

    detected_dimensions:
        [
            {
                "pixel_length": float,
                "real_length_inches": float
            }
        ]
    """

    if not detected_dimensions:
        return {
            "pixels_per_inch": None,
            "calibration_status": "NO DIMENSION DETECTED"
        }

    # Use first valid dimension for hackathon scope
    dim = detected_dimensions[0]

    pixel_length = dim.get("pixel_length")
    real_length_inches = dim.get("real_length_inches")

    if not pixel_length or not real_length_inches:
        return {
            "pixels_per_inch": None,
            "calibration_status": "INVALID DIMENSION DATA"
        }

    pixels_per_inch = pixel_length / real_length_inches

    return {
        "pixels_per_inch": round(pixels_per_inch, 4),
        "calibration_status": "CALIBRATED"
    }