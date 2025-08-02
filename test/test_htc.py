from hxforge.physics.htc import overall_htc, wall_resistance
import pytest


def test_overall_htc():
    """Test the overall heat transfer coefficient calculation."""
    htc1 = 100.0  # W/m²·K
    htc2 = 200.0  # W/m²·K
    R_wall = 0.05  # K·m²/W

    expected_htc = 1 / (1 / htc1 + R_wall + 1 / htc2)
    assert overall_htc(htc1, htc2, R_wall) == pytest.approx(expected_htc, rel=1e-12)


def test_overall_htc_invalid():
    """Test invalid inputs for overall heat transfer coefficient."""
    with pytest.raises(ValueError):
        overall_htc(-100.0, 200.0, 0.05)  # Negative htc1
    with pytest.raises(ValueError):
        overall_htc(100.0, -200.0, 0.05)  # Negative htc2
    with pytest.raises(ValueError):
        overall_htc(100.0, 200.0, -0.05)  # Negative R_wall


def test_wall_resistance():
    """Test the wall resistance calculation."""
    thickness = 0.1  # m
    k = 0.5  # W/(m·K)

    expected_resistance = thickness / k
    assert wall_resistance(thickness, k) == pytest.approx(
        expected_resistance, rel=1e-12
    )


def test_wall_resistance_invalid():
    """Test invalid inputs for wall resistance."""
    with pytest.raises(ValueError):
        wall_resistance(-0.1, 0.5)  # Negative thickness
    with pytest.raises(ValueError):
        wall_resistance(0.1, -0.5)  # Negative thermal conductivity
    with pytest.raises(ValueError):
        wall_resistance(0.0, 0.5)  # Zero thickness
    with pytest.raises(ValueError):
        wall_resistance(0.1, 0.0)  # Zero thermal conductivity
