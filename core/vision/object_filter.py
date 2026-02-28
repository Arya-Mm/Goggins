CLASS_MAP = {
    0: "column",
    1: "curtain_wall",
    2: "dimension",
    3: "door",
    4: "railing",
    5: "door",          # treat sliding door as door
    6: "stair",
    7: "wall",
    8: "window"
}


def filter_structural_objects(detections):

    filtered = []

    for d in detections:
        label = CLASS_MAP.get(d["class_id"], None)

        if label in ["wall", "door", "column"]:
            d["label"] = label
            filtered.append(d)

    return filtered