def build_structural_twin(detections, walls, dimensions, scale_factor):
    """
    Builds unified structural twin model.
    Combines detections + wall data + dimensions.
    """

    columns = detections.get("columns", [])
    beams = detections.get("beams", [])
    slabs = detections.get("slabs", [])

    twin = {
        "columns": [],
        "beams": [],
        "slabs": [],
        "walls": walls,
        "scale_factor": scale_factor,
        "confidence": detections.get("confidence", 0.8)
    }

    # Convert bbox to geometry with scale applied
    for col in columns:
        x1, y1, x2, y2 = col["bbox"]
        width = (x2 - x1) * scale_factor
        height = (y2 - y1) * scale_factor

        twin["columns"].append({
            "geometry": {
                "width": round(width, 3),
                "height": round(height, 3)
            },
            "confidence": col["confidence"]
        })

    for beam in beams:
        x1, y1, x2, y2 = beam["bbox"]
        length = (x2 - x1) * scale_factor

        twin["beams"].append({
            "geometry": {
                "length": round(length, 3)
            },
            "confidence": beam["confidence"]
        })

    for slab in slabs:
        x1, y1, x2, y2 = slab["bbox"]
        area = ((x2 - x1) * (y2 - y1)) * scale_factor

        twin["slabs"].append({
            "geometry": {
                "area": round(area, 3)
            },
            "confidence": slab["confidence"]
        })

    return twin