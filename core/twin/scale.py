import math

COMMON_DIMENSIONS = [
    (20, 30),
    (24, 36),
    (25, 40),
    (27, 37),
    (30, 40),
    (30, 45),
    (40, 60),
    (36, 36),
    (40, 40),
    (45, 50),
]


def calibrate_scale(blueprint, walls, dimensions):
    if not walls:
        return 1.0, 0.5

    horizontal_walls = [w for w in walls if w["orientation"] == "horizontal"]
    vertical_walls = [w for w in walls if w["orientation"] == "vertical"]

    if not horizontal_walls or not vertical_walls:
        return 1.0, 0.5

    # Select longest outer boundaries
    longest_horizontal = max(horizontal_walls, key=lambda w: w["length_pixels"])
    longest_vertical = max(vertical_walls, key=lambda w: w["length_pixels"])

    pixel_width = longest_horizontal["length_pixels"]
    pixel_height = longest_vertical["length_pixels"]

    pixel_ratio = pixel_width / pixel_height

    best_match = None
    min_error = 999

    for w, h in COMMON_DIMENSIONS:
        real_ratio = w / h
        error = abs(pixel_ratio - real_ratio)

        if error < min_error:
            min_error = error
            best_match = (w, h)

    # Accept only if reasonable match
    if min_error < 0.15:
        real_width = best_match[0]
        scale_factor = real_width / pixel_width
        return round(scale_factor, 6), 0.9

    return 1.0, 0.6