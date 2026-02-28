import re


def parse_feet(text):
    """
    Converts dimension string like 27' or 14'-0" into float feet.
    """
    match = re.match(r"(\d+)'(?:-?(\d+))?", text)
    if not match:
        return None

    feet = int(match.group(1))
    inches = int(match.group(2)) if match.group(2) else 0

    return feet + inches / 12.0


def calibrate_scale(blueprint, walls, dimensions):
    """
    Multi-strategy automatic scale calibration.
    """

    if not walls:
        return 1.0, 0.6

    # Longest horizontal and vertical walls
    horizontal = next((w for w in walls if w["orientation"] == "horizontal"), None)
    vertical = next((w for w in walls if w["orientation"] == "vertical"), None)

    best_scale = None
    confidence = 0.6

    # STRATEGY 1 — Boundary-based
    for dim in dimensions.get("dimensions", []):
        real_length = parse_feet(dim["text"])
        if real_length is None:
            continue

        if horizontal:
            pixel_length = horizontal["length_pixels"]
            scale = real_length / pixel_length
            best_scale = scale
            confidence = 0.92
            break

        if vertical:
            pixel_length = vertical["length_pixels"]
            scale = real_length / pixel_length
            best_scale = scale
            confidence = 0.92
            break

    # STRATEGY 2 — Fallback interior dimensions
    if best_scale is None:
        for dim in dimensions.get("dimensions", []):
            real_length = parse_feet(dim["text"])
            if real_length is None:
                continue

            # Approximate against longest wall
            pixel_length = walls[0]["length_pixels"]
            scale = real_length / pixel_length
            best_scale = scale
            confidence = 0.8
            break

    if best_scale is None:
        return 1.0, 0.6

    return round(best_scale, 6), confidence