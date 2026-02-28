def compute_quantities(structural_twin):

    total_wall_volume = 0
    total_wall_length = 0

    for wall in structural_twin["walls"]:
        total_wall_volume += wall["volume_m3"]
        total_wall_length += wall["length_m"]

    return {
        "total_wall_length_m": round(total_wall_length, 2),
        "total_wall_volume_m3": round(total_wall_volume, 2)
    }