import math


class StructuralTwinBuilder:

    def __init__(self, min_confidence=0.3):
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

    def _match_dimension(self, wall_bbox, dimensions, threshold=150):
        if not dimensions:
            return None, True

        nearest = min(
            dimensions,
            key=lambda d: self._distance(wall_bbox, d["bbox"])
        )

        distance = self._distance(wall_bbox, nearest["bbox"])

        if distance > threshold:
            return None, True

        return nearest["inches"], False

    def _openings_for_wall(self, wall_bbox, openings, threshold=120):
        assigned = []
        for op in openings:
            if self._distance(wall_bbox, op["bbox"]) < threshold:
                assigned.append(op)
        return assigned

    # ----------------------------
    # Quantity Computation
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
                wall["gross_volume_cuft"] = 0
                wall["net_volume_cuft"] = 0
                continue

            gross_cuin = length * WALL_HEIGHT * WALL_THICKNESS

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
    # Confidence & Buildability
    # ----------------------------

    def compute_scores(self, twin, dimensions):

        # -------------------------
        # Detection Confidence
        # -------------------------

        def avg_conf(objs):
            if not objs:
                return 0
            return sum(o["confidence"] for o in objs) / len(objs)

        wall_conf = avg_conf(twin["walls"])
        door_conf = avg_conf(twin["doors"])
        window_conf = avg_conf(twin["windows"])

        dimension_score = 1 if dimensions else 0

        twin["confidence_score"] = round(
            (wall_conf * 50 + door_conf * 20 + window_conf * 10 + dimension_score * 20),
            2
        )

        # -------------------------
        # Buildability Score
        # -------------------------

        score = 100

        # Penalize uncertainty
        uncertain_walls = sum(
            1 for w in twin["walls"]
            if w.get("dimension_uncertain", False)
        )

        score -= uncertain_walls * 5

        # Penalize zero volume
        if twin["total_net_wall_volume_cuft"] == 0:
            score -= 20

        # Penalize excessive door density
        if len(twin["walls"]) > 0:
            if len(twin["doors"]) > len(twin["walls"]) * 6:
                score -= 10

        score = max(0, min(100, score))

        twin["buildability_score"] = score

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

        for obj in raw_walls:
            if obj["confidence"] >= self.min_confidence:

                real_length, uncertain = self._match_dimension(
                    obj["bbox"], dimensions
                )

                walls.append({
                    "length_inches": real_length,
                    "confidence": obj["confidence"],
                    "bbox": obj["bbox"],
                    "dimension_uncertain": uncertain
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
        twin = self.compute_scores(twin, dimensions)

        twin["summary"] = {
            "wall_count": len(walls),
            "door_count": len(doors),
            "window_count": len(windows),
            "net_volume_cuft": twin["total_net_wall_volume_cuft"],
            "estimated_bricks": twin["estimated_bricks"],
            "confidence_score": twin["confidence_score"],
            "buildability_score": twin["buildability_score"],
            "uncertain_walls": sum(
                1 for w in walls if w.get("dimension_uncertain", False)
            )
        }

        return twin