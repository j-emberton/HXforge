"""
heat_load_dash.py — Dash UI wrapping the Rust `heat_load_lmtd` function

Compatible with dash‑bootstrap‑components ≥ 1.0 (no deprecated FormGroup).

Usage
-----
Development:
    python heat_load_dash.py
Production / WSGI:
    gunicorn 'heat_load_dash:create_app()'
Tests can simply import `create_app()` or the module‑level `app`.
"""

from __future__ import annotations

from dash import Dash, html, Input, Output, State
import dash_bootstrap_components as dbc
import hxforge.gui.layout as layout

# ──────────────────────────────────────────────────────────────────────────────
# Native extension (Rust via PyO3) — adjust import to your wheel name.
# ──────────────────────────────────────────────────────────────────────────────
from hxforge_solver import heat_load_lmtd as lmtd  # type: ignore
from hxforge.physics.htc import overall_htc, wall_resistance  # type: ignore

# Default input values
DEFAULT_HTC_EXT = 500.0  # W/m²·K
DEFAULT_HTC_INT = 1000.0  # W/m²·K
DEFAULT_TUBE_LEN = 1  # m
DEFAULT_TUBE_DIAM_EXT = 0.002  # m
DEFAULT_TUBE_THK = 0.0005  # m
DEFAULT_DT1 = 30.0  # K
DEFAULT_DT2 = 20.0  # K


# ╭──────────────────────────────────────────────────────────────────────────╮
# │ Dash App Factory                                                        │
# ╰──────────────────────────────────────────────────────────────────────────╯


def create_app() -> Dash:
    """Return a fully configured Dash app instance."""

    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        title="Heat‑Load (LMTD) Calculator",
    )

    app.layout = layout.build_layout_manager()
    _register_callbacks(app)
    return app


# ╭──────────────────────────────────────────────────────────────────────────╮
# │ Callbacks                                                               │
# ╰──────────────────────────────────────────────────────────────────────────╯


def _register_callbacks(app: Dash) -> None:
    """Bind server callbacks to *app*."""

    @app.callback(
        Output("output-q", "children"),
        Input("btn-calc", "n_clicks"),
        State("input-htc-ext", "value"),
        State("input-htc-int", "value"),
        State("input-tube-len", "value"),
        State("input-tube-diam-ext", "value"),
        State("input-tube-thk", "value"),
        State("input-dt1", "value"),
        State("input-dt2", "value"),
        prevent_initial_call=True,
    )
    def _prep_and_run_case(
        _clicks: int | None,
        htc_ext: float | None,
        htc_int: float | None,
        tube_len: float | None,
        tube_diam_ext: float | None,
        tube_thk: float | None,
        dt1: float | None,
        dt2: float | None,
    ) -> str:
        if None in (htc_ext, htc_int, tube_len, tube_diam_ext, tube_thk, dt1, dt2):
            return "Please fill in all inputs."
        else:
            try:
                u = overall_htc(
                    float(htc_ext),
                    float(htc_int),
                    wall_resistance(float(tube_thk), 0.5),  # Assume k = 0.5 W/(m·K)
                )
                watts = lmtd(float(u), float(area), float(dt1), float(dt2))
                return f"{watts:,.2f} W"
            except Exception as exc:  # pragma: no cover — display to user
                return f"Error: {exc}"
            
        def _validate_inputs(
            htc_ext, htc_int, tube_len, tube_diam_ext, tube_thk, dt1, dt2
        ) 


            
        


# Expose a module‑level `app` so `python heat_load_dash.py` just works.
app = create_app()


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True, host="0.0.0.0", port=8050)
