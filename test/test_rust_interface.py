import math
import hxforge_solver  # adjust to match your Cargo project name


def test_generic_case():
    q = hxforge_solver.heat_load_lmtd(500.0, 12.0, 40.0, 20.0)
    expected = 500.0 * 12.0 * (40.0 - 20.0) / math.log(40.0 / 20.0)
    assert math.isclose(q, expected, rel_tol=1e-12)


def test_equal_deltas():
    q = hxforge_solver.heat_load_lmtd(650.0, 8.5, 30.0, 30.0)
    assert math.isclose(q, 650.0 * 8.5 * 30.0, rel_tol=1e-12)
