use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
/// Calculate Log Mean Temperature Difference (LMTD) heat load.
/// Returns `q = U · A · LMTD`.
#[pyfunction]
pub fn heat_load_lmtd(u: f64, area: f64, delta_t1: f64, delta_t2: f64) -> f64 {
    let lmtd = if (delta_t1 - delta_t2).abs() < 1e-12 {
        // avoid division-by-zero when ΔT1 ≈ ΔT2
        delta_t1
    } else {
        (delta_t1 - delta_t2) / ((delta_t1 / delta_t2).ln())
    };
    u * area * lmtd
}

#[cfg(test)]
mod test_heat_load_lmtd {
    use super::heat_load_lmtd;

    /// Assert two f64 numbers are within ±ε.
    fn assert_close(left: f64, right: f64, eps: f64) {
        if (left - right).abs() > eps {
            panic!("|{left} - {right}| > {eps}");
        }
    }

    #[test]
    fn generic_case() {
        let (u, a, dt1, dt2) = (500.0, 12.0, 40.0, 20.0);
        let q = heat_load_lmtd(u, a, dt1, dt2);

        let lmtd = (dt1 - dt2) / (dt1 / dt2).ln();
        let expected = u * a * lmtd;

        assert_close(q, expected, 1e-9);
    }

    #[test]
    fn equal_deltas() {
        let (u, a, dt) = (650.0, 8.5, 30.0);
        let q = heat_load_lmtd(u, a, dt, dt);

        let expected = u * a * dt;
        assert_close(q, expected, 1e-9);
    }
}


/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn hxforge_solver(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(heat_load_lmtd, m)?)?;
    Ok(())
}

