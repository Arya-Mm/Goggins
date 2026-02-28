import math


class StructuralTwinBuilder:

    def __init__(self, min_confidence=0.5):
        self.min_confidence = min_confidence

    # ----------------------------
    # Utility Functions
    # ----------------------------

    def _bbox_center(self, bbox):
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    def _distance(self, b1, b2):
        c1 = self._bbox_center(b1)
        c2 = self._bbox_center(b2)
        return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)

    def _match_dimension(self, wall_bbox, dimensions):
        """
        Assign nearest detected dimension to a wall.
        """
        if not dimensions:
            return None

        nearest = min(
            dimensions,
            key=lambda d: self._distance(wall_bbox, d["bbox"])
        )

        return nearest["inches"]

    # ----------------------------
    # Quantity Intelligence
    # ----------------------------

    def compute_quantities(self, twin):

        # Assumptions (can be made configurable later)
        WALL_HEIGHT_INCHES = 120  # 10 ft
        WALL_THICKNESS_INCHES = 9  # 9 inch brick wall

        DOOR_WIDTH = 36
        DOOR_HEIGHT = 84

        WINDOW_WIDTH = 48
        WINDOW_HEIGHT = 48

        total_wall_volume_cuin = 0

        # ---- WALL GROSS VOLUME ----
        for wall in twin["walls"]:
            length = wall["length_inches"]

            if length is None:
                continue

            wall_volume_cuin = (
                length * WALL_HEIGHT_INCHES * WALL_THICKNESS_INCHES
            )

            wall["volume_cuft"] = round(wall_volume_cuin / 1728, 2)

            total_wall_volume_cuin += wall_volume_cuin

        gross_volume_cuft = total_wall_volume_cuin / 1728

        # ---- OPENING DEDUCTIONS ----
        door_volume_cuin = (
            DOOR_WIDTH * DOOR_HEIGHT * WALL_THICKNESS_INCHES
        ) * len(twin["doors"])

        window_volume_cuin = (
            WINDOW_WIDTH * WINDOW_HEIGHT * WALL_THICKNESS_INCHES
        ) * len(twin["windows"])

        opening_volume_cuin = door_volume_cuin + window_volume_cuin
        opening_volume_cuft = opening_volume_cuin / 1728

        # ---- NET VOLUME ----
        net_volume_cuft = gross_volume_cuft - opening_volume_cuft

        if net_volume_cuft < 0:
            net_volume_cuft = 0

        twin["gross_wall_volume_cuft"] = round(gross_volume_cuft, 2)
        twin["opening_volume_cuft"] = round(opening_volume_cuft, 2)
        twin["net_wall_volume_cuft"] = round(net_volume_cuft, 2)

        # Brick estimation (industry approx)
        twin["estimated_bricks"] = int(net_volume_cuft * 13.5)

        return twin

    # ----------------------------
    # Main Twin Builder
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

        # ---- WALLS ----
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

        twin = self.compute_quantities(twin)

        return twin