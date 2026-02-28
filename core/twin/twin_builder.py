import math


class StructuralTwinBuilder:

    def __init__(self):
        pass

    # -------------------------
    # Estimate Scale
    # -------------------------
    def estimate_scale(self, dimensions):
        """
        Estimate pixel-to-inch scale using longest dimension.
        """
        if not dimensions:
            return 1.0  # fallback

        # Choose largest real dimension
        largest = max(dimensions, key=lambda d: d["inches"])
        real_inches = largest["inches"]

        x0, y0, x1, y1 = largest["bbox"]
        pixel_length = math.dist((x0, y0), (x1, y1))

        if pixel_length == 0:
            return 1.0

        return real_inches / pixel_length

    # -------------------------
    # Convert Walls to Geometry
    # -------------------------
    def build_walls(self, wall_detections, scale):
        walls = []

        for wall in wall_detections:
            x0, y0, x1, y1 = wall["bbox"]

            pixel_length = math.dist((x0, y0), (x1, y1))
            real_length = pixel_length * scale

            walls.append({
                "length_inches": round(real_length, 2),
                "confidence": wall["confidence"],
                "bbox": wall["bbox"]
            })

        return walls

    # -------------------------
    # Build Twin
    # -------------------------
    def build(self, vision_output):

        dimensions = vision_output.get("dimensions", [])
        objects = vision_output.get("objects", {})

        scale = self.estimate_scale(dimensions)

        walls = self.build_walls(objects.get("walls", []), scale)

        twin = {
            "scale_factor": round(scale, 4),
            "walls": walls,
            "doors": objects.get("doors", []),
            "windows": objects.get("windows", []),
            "columns": objects.get("columns", []),
            "beams": objects.get("beams", []),
            "slabs": objects.get("slabs", [])
        }

        return twin