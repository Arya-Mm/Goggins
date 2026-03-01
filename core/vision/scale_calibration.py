# core/vision/scale_calibration.py

def calibrate_scale(detected_dimensions):

    # If no dimensions detected, assume default DPI silently
    if not detected_dimensions:
        return {
            "pixels_per_inch": 96,
            "calibration_status": "DEFAULT_SCALE_APPLIED"
        }

    dim = detected_dimensions[0]

    pixel_length = dim.get("pixel_length")
    real_length_inches = dim.get("real_length_inches")

    if not pixel_length or not real_length_inches:
        return {
            "pixels_per_inch": 96,
            "calibration_status": "DEFAULT_SCALE_APPLIED"
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
            "calibration_status": "DEFAULT_SCALE_APPLIED"
        }