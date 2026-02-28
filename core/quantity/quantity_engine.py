import math


def calculate_quantities(twin, rates=None):
    """
    Deterministic Quantity & Cost Estimation Engine
    Fully auditable and hackathon-safe.
    """

    if rates is None:
        # Default Indian approximate construction rates (can be slider controlled later)
        rates = {
            "concrete_per_cuft": 120,       # ₹ per cubic foot
            "brick_per_unit": 8,            # ₹ per brick
            "steel_per_kg": 70,             # ₹ per kg
            "plaster_per_sqft": 25          # ₹ per sqft
        }

    # ===============================
    # WALL QUANTITIES
    # ===============================

    total_wall_volume = twin.get("total_net_wall_volume_cuft", 0)
    total_bricks = twin.get("estimated_bricks", 0)

    # Steel estimation (simple ratio assumption)
    # 1% steel ratio assumption for masonry structures
    estimated_steel_kg = round(total_wall_volume * 2.5, 2)

    # Plaster area (2 sides of wall)
    plaster_area_sqft = round(total_wall_volume * 2, 2)

    # ===============================
    # COST CALCULATIONS
    # ===============================

    concrete_cost = round(total_wall_volume * rates["concrete_per_cuft"], 2)
    brick_cost = round(total_bricks * rates["brick_per_unit"], 2)
    steel_cost = round(estimated_steel_kg * rates["steel_per_kg"], 2)
    plaster_cost = round(plaster_area_sqft * rates["plaster_per_sqft"], 2)

    total_cost = round(
        concrete_cost + brick_cost + steel_cost + plaster_cost,
        2
    )

    # ===============================
    # PHASE-WISE BREAKDOWN
    # ===============================

    phase_breakdown = {
        "foundation_phase": {
            "concrete_cuft": round(total_wall_volume * 0.3, 2),
            "estimated_cost": round(total_cost * 0.3, 2)
        },
        "superstructure_phase": {
            "concrete_cuft": round(total_wall_volume * 0.5, 2),
            "estimated_cost": round(total_cost * 0.5, 2)
        },
        "finishing_phase": {
            "plaster_sqft": plaster_area_sqft,
            "estimated_cost": round(total_cost * 0.2, 2)
        }
    }

    # ===============================
    # FINAL OUTPUT STRUCTURE
    # ===============================

    return {
        "material_quantities": {
            "wall_volume_cuft": total_wall_volume,
            "estimated_bricks": total_bricks,
            "estimated_steel_kg": estimated_steel_kg,
            "plaster_area_sqft": plaster_area_sqft
        },
        "cost_breakdown": {
            "concrete_cost": concrete_cost,
            "brick_cost": brick_cost,
            "steel_cost": steel_cost,
            "plaster_cost": plaster_cost,
            "total_project_cost": total_cost
        },
        "phase_breakdown": phase_breakdown,
        "rates_used": rates
    }