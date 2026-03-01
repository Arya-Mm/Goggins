# core/vision/scale_calibration.py

def calibrate_scale(detected_dimensions):
    """
    Converts pixel length to real-world scale.

    detected_dimensions:
        [
            {
                "pixel_length": float,
                "real_length_inches": float
            }
        ]
    """

    # No dimension detected
    if not detected_dimensions:
        return {
            "pixels_per_inch": 96,  # Safe assumed DPI
            "calibration_status": "ASSUMED_DEFAULT_SCALE"
        }

    dim = detected_dimensions[0]

    pixel_length = dim.get("pixel_length")
    real_length_inches = dim.get("real_length_inches")

    if not pixel_length or not real_length_inches:
        return {
            "pixels_per_inch": 96,
            "calibration_status": "ASSUMED_INVALID_INPUT"
        }

    try:
        pixels_per_inch = pixel_length / real_length_inches

        return {
            "pixels_per_inch": round(pixels_per_inch, 4),
            "calibration_status": "CALIBRATED"
        }

    except:
        return {
            "pixels_per_inch": 96,
            "calibration_status": "ASSUMED_FALLBACK"
        }