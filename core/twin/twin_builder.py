import random

class StructuralTwin:
    def __init__(self, columns, beams, slabs):
        self.columns = columns
        self.beams = beams
        self.slabs = slabs

    def to_dict(self):
        return {
            "columns": self.columns,
            "beams": self.beams,
            "slabs": self.slabs
        }


def build_structural_twin():
    """
    Temporary deterministic twin generator.
    Replace later with YOLO + OCR extraction.
    """

    # Minimal controlled randomness for demo realism
    columns = random.randint(6, 12)
    beams = columns + random.randint(4, 10)
    slabs = random.randint(2, 5)

    return StructuralTwin(columns, beams, slabs)