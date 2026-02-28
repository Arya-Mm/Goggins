import math


class StructuralTwinBuilder:

    def __init__(self, min_confidence=0.5):
        self.min_confidence = min_confidence

    def _bbox_center(self, bbox):
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    def _distance(self, b1, b2):
        c1 = self._bbox_center(b1)
        c2 = self._bbox_center(b2)
        return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

    def _match_dimension(self, wall_bbox, dimensions):
        """
        Assign nearest dimension to wall.
        """
        if not dimensions:
            return None

        nearest = min(
            dimensions,
            key=lambda d: self._distance(wall_bbox, d["bbox"])
        )

        return nearest["inches"]

    def build(self, vision_output):

        dimensions = vision_output.get("dimensions", [])
        objects = vision_output.get("objects", {})

        walls = []
        doors = []
        windows = []

        raw_walls = objects.get("walls", [])
        raw_doors = objects.get("doors", [])
        raw_windows = objects.get("windows", [])

        # ---- WALLS ----
        for obj in raw_walls:
            if obj["confidence"] < self.min_confidence:
                continue

            real_length = self._match_dimension(obj["bbox"], dimensions)

            walls.append({
                "length_inches": real_length,
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
            "walls": walls,
            "doors": doors,
            "windows": windows,
            "columns": objects.get("columns", []),
            "beams": objects.get("beams", []),
            "slabs": objects.get("slabs", [])
        }

        return twin