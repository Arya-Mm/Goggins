from core.ingestion.loader import BlueprintLoader

loader = BlueprintLoader()
result = loader.load("test_blueprint.png")

print("Loaded:", result["success"])
print("Image size:", result["width"], "x", result["height"])