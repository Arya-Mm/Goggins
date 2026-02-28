import math


COMMON_DIMENSIONS = [
    (20, 30),
    (24, 36),
    (25, 40),
    (27, 37),
    (30, 40),
    (30, 45),
    (40, 60)
]


def calibrate_scale(blueprint, walls, dimensions):
    if not walls:
        return 1.0, 0.6

    horizontal = next((w for w in walls if w["orientation"] == "horizontal"), None)
    vertical = next((w for w in walls if w["orientation"] == "vertical"), None)

    if not horizontal or not vertical:
        return 1.0, 0.6

    pixel_width = horizontal["length_pixels"]
    pixel_height = vertical["length_pixels"]

    pixel_ratio = pixel_width / pixel_height

    best_match = None
    min_error = 999

    for w, h in COMMON_DIMENSIONS:
        real_ratio = w / h
        error = abs(pixel_ratio - real_ratio)

        if error < min_error:
            min_error = error
            best_match = (w, h)

    # Accept match if close enough
    if min_error < 0.1:
        real_width = best_match[0]
        scale_factor = real_width / pixel_width
        return round(scale_factor, 6), 0.9

    return 1.0, 0.6