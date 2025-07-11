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

# ──────────────────────────────────────────────────────────────────────────────
# Native extension (Rust via PyO3) — adjust import to your wheel name.
# ──────────────────────────────────────────────────────────────────────────────
from hxforge_solver import heat_load_lmtd as lmtd  # type: ignore

# Default input values
DEFAULT_U = 500.0  # W/m²·K
DEFAULT_AREA = 10.0  # m²
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

    app.layout = _build_layout()
    _register_callbacks(app)
    return app


# ╭──────────────────────────────────────────────────────────────────────────╮
# │ Layout Builders                                                         │
# ╰──────────────────────────────────────────────────────────────────────────╯


def _build_layout() -> dbc.Container:
    """Construct page layout (pure function)."""

    def _num(id_: str, label: str, value: float, step: float) -> html.Div:
        """Create a labelled numeric input (no deprecated FormGroup)."""
        return html.Div(
            [
                dbc.Label(label, html_for=id_, className="form-label mb-1"),
                dbc.Input(
                    id=id_,
                    type="number",
                    value=value,
                    step=step,
                    debounce=True,
                    className="form-control",
                ),
            ],
            className="mb-2",
        )

    inputs = dbc.Card(
        [
            dbc.CardHeader(html.H5("Inputs")),
            dbc.CardBody(
                [
                    _num("input-u", "Overall U (W/m²·K)", DEFAULT_U, 0.1),
                    _num("input-area", "Area A (m²)", DEFAULT_AREA, 0.01),
                    _num("input-dt1", "ΔT₁ (K)", DEFAULT_DT1, 0.1),
                    _num("input-dt2", "ΔT₂ (K)", DEFAULT_DT2, 0.1),
                    dbc.Button(
                        "Calculate", id="btn-calc", color="primary", className="mt-3"
                    ),
                ]
            ),
        ],
        className="shadow-sm",
    )

    output = dbc.Card(
        [
            dbc.CardHeader(html.H5("Heat Duty Q")),
            dbc.CardBody(html.H2(id="output-q", className="text-primary my-0")),
        ],
        className="shadow-sm",
    )

    return dbc.Container(
        [
            html.H2("Heat‑Load (LMTD) Calculator", className="my-4"),
            dbc.Row(
                [
                    dbc.Col(inputs, width=4),
                    dbc.Col(output, width=8),
                ]
            ),
        ],
        fluid=True,
        className="px-4",
    )


# ╭──────────────────────────────────────────────────────────────────────────╮
# │ Callbacks                                                               │
# ╰──────────────────────────────────────────────────────────────────────────╯


def _register_callbacks(app: Dash) -> None:
    """Bind server callbacks to *app*."""

    @app.callback(
        Output("output-q", "children"),
        Input("btn-calc", "n_clicks"),
        State("input-u", "value"),
        State("input-area", "value"),
        State("input-dt1", "value"),
        State("input-dt2", "value"),
        prevent_initial_call=True,
    )
    def _calculate_heat(
        _clicks: int | None,
        u: float | None,
        area: float | None,
        dt1: float | None,
        dt2: float | None,
    ) -> str:
        if None in (u, area, dt1, dt2):
            return "Please fill in all inputs."
        try:
            watts = lmtd(float(u), float(area), float(dt1), float(dt2))
            return f"{watts:,.2f} W"
        except Exception as exc:  # pragma: no cover — display to user
            return f"Error: {exc}"


# Expose a module‑level `app` so `python heat_load_dash.py` just works.
app = create_app()


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True, host="0.0.0.0", port=8050)

