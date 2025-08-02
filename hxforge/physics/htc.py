"""Standard mathematical operations for htc and tehrmal resistance calculations"""


def overall_htc(htc1: float, htc2: float, R_wall: float) -> float:
    """Calculate the overall heat transfer coefficient."""
    if htc1 <= 0 or htc2 <= 0 or R_wall < 0:
        raise ValueError(
            "Heat transfer coefficients must be positive and wall resistance non-negative."
        )

    return 1 / (1 / htc1 + R_wall + 1 / htc2)


def wall_resistance(thickness: float, k: float) -> float:
    """Calculate the wall resistance.

    Args:
        thickness (float): Thickness of the wall in meters.
        k (float): Thermal conductivity of the wall material in W/(m·K).
    Returns:
        Wall resistance in K·m²/W."""

    if thickness <= 0 or k <= 0:
        raise ValueError("Thickness and thermal conductivity must be positive.")

    return thickness / k
