import math


class StructuralTwinBuilder:

    def __init__(self, min_confidence=0.5):
        self.min_confidence = min_confidence

    # ----------------------------
    # Geometry Utilities
    # ----------------------------

    def _bbox_center(self, bbox):
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    def _distance(self, b1, b2):
        c1 = self._bbox_center(b1)
        c2 = self._bbox_center(b2)
        return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)

    def _match_dimension(self, wall_bbox, dimensions):
        if not dimensions:
            return None

        nearest = min(
            dimensions,
            key=lambda d: self._distance(wall_bbox, d["bbox"])
        )

        return nearest["inches"]

    def _openings_for_wall(self, wall_bbox, openings, threshold=120):
        """
        Assign openings to a wall if they are spatially close.
        """
        assigned = []

        for op in openings:
            dist = self._distance(wall_bbox, op["bbox"])
            if dist < threshold:
                assigned.append(op)

        return assigned

    # ----------------------------
    # Quantity Engine
    # ----------------------------

    def compute_quantities(self, twin):

        WALL_HEIGHT = 120
        WALL_THICKNESS = 9

        DOOR_WIDTH = 36
        DOOR_HEIGHT = 84

        WINDOW_WIDTH = 48
        WINDOW_HEIGHT = 48

        total_net_volume = 0

        for wall in twin["walls"]:

            length = wall["length_inches"]
            if length is None:
                continue

            gross_cuin = length * WALL_HEIGHT * WALL_THICKNESS

            # Find openings belonging to this wall
            doors = self._openings_for_wall(
                wall["bbox"], twin["doors"]
            )

            windows = self._openings_for_wall(
                wall["bbox"], twin["windows"]
            )

            door_volume = (
                DOOR_WIDTH * DOOR_HEIGHT * WALL_THICKNESS
            ) * len(doors)

            window_volume = (
                WINDOW_WIDTH * WINDOW_HEIGHT * WALL_THICKNESS
            ) * len(windows)

            net_cuin = gross_cuin - (door_volume + window_volume)

            if net_cuin < 0:
                net_cuin = 0

            wall["gross_volume_cuft"] = round(gross_cuin / 1728, 2)
            wall["net_volume_cuft"] = round(net_cuin / 1728, 2)
            wall["attached_doors"] = len(doors)
            wall["attached_windows"] = len(windows)

            total_net_volume += net_cuin / 1728

        twin["total_net_wall_volume_cuft"] = round(total_net_volume, 2)
        twin["estimated_bricks"] = int(total_net_volume * 13.5)

        return twin

    # ----------------------------
    # Main Builder
    # ----------------------------

    def build(self, vision_output):

        dimensions = vision_output.get("dimensions", [])
        objects = vision_output.get("objects", {})

        walls = []
        doors = []
        windows = []

        raw_walls = objects.get("walls", [])
        raw_doors = objects.get("doors", [])
        raw_windows = objects.get("windows", [])

        for obj in raw_walls:
            if obj["confidence"] < self.min_confidence:
                continue

            real_length = self._match_dimension(
                obj["bbox"], dimensions
            )

            walls.append({
                "length_inches": real_length,
                "confidence": obj["confidence"],
                "bbox": obj["bbox"]
            })

        for obj in raw_doors:
            if obj["confidence"] >= self.min_confidence:
                doors.append(obj)

        for obj in raw_windows:
            if obj["confidence"] >= self.min_confidence:
                windows.append(obj)

        twin = {
            "walls": walls,
            "doors": doors,
            "windows": windows,
            "columns": objects.get("columns", []),
            "beams": objects.get("beams", []),
            "slabs": objects.get("slabs", [])
        }

        twin = self.compute_quantities(twin)

        return twin