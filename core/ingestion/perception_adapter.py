import uuid
import json

class StructuralTwinBuilder:

    def __init__(self, scale_pixels_per_meter):
        self.scale = scale_pixels_per_meter

    def px_to_m(self, value_px):
        return value_px / self.scale

    def build_column(self, bbox, confidence):
        x, y, w, h = bbox
        return {
            "id": f"C-{uuid.uuid4().hex[:6]}",
            "position": {
                "x": self.px_to_m(x),
                "y": self.px_to_m(y)
            },
            "dimensions": {
                "width_m": self.px_to_m(w),
                "depth_m": self.px_to_m(h)
            },
            "confidence": round(float(confidence), 3)
        }

    def build_beam(self, start_px, end_px, confidence):
        x1, y1 = start_px
        x2, y2 = end_px

        length_m = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        length_m = self.px_to_m(length_m)

        return {
            "id": f"B-{uuid.uuid4().hex[:6]}",
            "start": {"x": self.px_to_m(x1), "y": self.px_to_m(y1)},
            "end": {"x": self.px_to_m(x2), "y": self.px_to_m(y2)},
            "length_m": round(length_m, 3),
            "confidence": round(float(confidence), 3)
        }

    def assemble_project(self, columns, beams, slabs, walls):
        return {
            "meta": {
                "project_id": str(uuid.uuid4()),
                "scale": {
                    "pixels_per_meter": self.scale,
                    "confidence": 0.9
                }
            },
            "elements": {
                "columns": columns,
                "beams": beams,
                "slabs": slabs,
                "walls": walls
            }
        }

    def save(self, twin_data, path="project_twin.json"):
        with open(path, "w") as f:
            json.dump(twin_data, f, indent=2)