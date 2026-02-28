import math


DEFAULT_WALL_THICKNESS = 0.2  # meters
DEFAULT_WALL_HEIGHT = 3.0     # meters


def build_structural_twin(detections, walls, dimensions, scale_factor):

    structured_walls = []
    total_confidence = []

    for w in walls:

        real_length = w["length_pixels"] * scale_factor

        volume = real_length * DEFAULT_WALL_THICKNESS * DEFAULT_WALL_HEIGHT

        structured_walls.append({
            "start": w["start"],
            "end": w["end"],
            "orientation": w["orientation"],
            "length_m": round(real_length, 3),
            "thickness_m": DEFAULT_WALL_THICKNESS,
            "height_m": DEFAULT_WALL_HEIGHT,
            "volume_m3": round(volume, 3),
            "confidence": w["confidence"]
        })

        total_confidence.append(w["confidence"])

    overall_conf = sum(total_confidence) / len(total_confidence) if total_confidence else 0.5

    return {
        "columns": [],
        "beams": [],
        "slabs": [],
        "walls": structured_walls,
        "scale_factor": scale_factor,
        "confidence": round(overall_conf, 3)
    }