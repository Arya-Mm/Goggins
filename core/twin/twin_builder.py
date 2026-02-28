import math


class StructuralTwinBuilder:

    def __init__(self, min_confidence=0.45):
        self.min_confidence = min_confidence

    def _compute_scale_factor(self, dimensions):
        """
        Compute scale factor using detected dimension annotations.
        Uses first valid dimension.
        """
        if not dimensions:
            return 1.0  # fallback

        # Take first dimension
        dim = dimensions[0]

        x1, y1, x2, y2 = dim["bbox"]
        pixel_length = abs(x2 - x1)

        if pixel_length == 0:
            return 1.0

        return dim["inches"] / pixel_length

    def _compute_wall_length(self, bbox, scale_factor):
        """
        Compute wall length using dominant axis (not diagonal).
        """
        x1, y1, x2, y2 = bbox

        width = abs(x2 - x1)
        height = abs(y2 - y1)

        wall_pixels = max(width, height)

        return round(wall_pixels * scale_factor, 2)

    def build(self, vision_output):

        dimensions = vision_output.get("dimensions", [])
        objects = vision_output.get("objects", {})

        scale_factor = self._compute_scale_factor(dimensions)

        walls = []
        doors = []
        windows = []

        # Handle grouped object format
        raw_walls = objects.get("walls", [])
        raw_doors = objects.get("doors", [])
        raw_windows = objects.get("windows", [])

        # ---- WALLS ----
        for obj in raw_walls:
            if obj["confidence"] < self.min_confidence:
                continue

            length_inches = self._compute_wall_length(
                obj["bbox"], scale_factor
            )

            walls.append({
                "length_inches": length_inches,
                "confidence": obj["confidence"],
                "bbox": obj["bbox"]
            })

        # ---- DOORS ----
        for obj in raw_doors:
            if obj["confidence"] < self.min_confidence:
                continue

            doors.append(obj)

        # ---- WINDOWS ----
        for obj in raw_windows:
            if obj["confidence"] < self.min_confidence:
                continue

            windows.append(obj)

        twin = {
            "scale_factor": round(scale_factor, 4),
            "walls": walls,
            "doors": doors,
            "windows": windows,
            "columns": objects.get("columns", []),
            "beams": objects.get("beams", []),
            "slabs": objects.get("slabs", [])
        }

        return twin