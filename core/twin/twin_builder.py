import math


DEFAULT_WALL_THICKNESS = 0.2  # meters
DEFAULT_WALL_HEIGHT = 3.0     # meters
PARALLEL_TOLERANCE = 5        # pixels
MIN_WALL_LENGTH_M = 2.5       # minimum structural wall length


def are_parallel_duplicates(w1, w2):
    if w1["orientation"] != w2["orientation"]:
        return False

    if abs(w1["length_pixels"] - w2["length_pixels"]) > 10:
        return False

    if w1["orientation"] == "vertical":
        return abs(w1["start"][0] - w2["start"][0]) < PARALLEL_TOLERANCE

    if w1["orientation"] == "horizontal":
        return abs(w1["start"][1] - w2["start"][1]) < PARALLEL_TOLERANCE

    return False


def deduplicate_walls(walls):
    filtered = []
    used = set()

    for i, w1 in enumerate(walls):
        if i in used:
            continue

        cluster = [w1]

        for j, w2 in enumerate(walls):
            if i == j or j in used:
                continue

            if are_parallel_duplicates(w1, w2):
                cluster.append(w2)
                used.add(j)

        main_wall = max(cluster, key=lambda w: w["length_pixels"])
        filtered.append(main_wall)

    return filtered


def build_structural_twin(detections, walls, dimensions, scale_factor):

    # Step 1 — Deduplicate
    walls = deduplicate_walls(walls)

    structured_walls = []
    total_confidence = []
    total_length_m = 0

    for w in walls:

        real_length = w["length_pixels"] * scale_factor

        # 🔥 Structural filter (ignore micro fragments)
        if real_length < MIN_WALL_LENGTH_M:
            continue

        volume = real_length * DEFAULT_WALL_THICKNESS * DEFAULT_WALL_HEIGHT

        structured_walls.append({
            "orientation": w["orientation"],
            "length_m": round(real_length, 3),
            "thickness_m": DEFAULT_WALL_THICKNESS,
            "height_m": DEFAULT_WALL_HEIGHT,
            "volume_m3": round(volume, 3),
            "confidence": w["confidence"]
        })

        total_confidence.append(w["confidence"])
        total_length_m += real_length

    if total_confidence:
        overall_conf = sum(total_confidence) / len(total_confidence)
    else:
        overall_conf = 0.5

    return {
        "columns": [],
        "beams": [],
        "slabs": [],
        "walls": structured_walls,
        "scale_factor": scale_factor,
        "total_wall_length_m": round(total_length_m, 2),
        "confidence": round(overall_conf, 3)
    }