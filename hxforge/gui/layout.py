import abc

def class Layout(abc.ABC):
    @abc.abstractmethod
    def _num(self, id_: str, label: str, value: float, step: float) -> html.Div:
        """Create a labelled numeric input (no deprecated FormGroup)."""
        pass

def class LMTD(Layout):
    """Layout builder for the LMTD calculator page."""

    def _num(self, id_: str, label: str, value: float, step: float) -> html.Div:
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
    
    def _generate_inputs(self):

        inputs = dbc.Card(
        [
            dbc.CardHeader(html.H5("Inputs")),
            dbc.CardBody(
                [
                    _num(
                        "input-htc-ext", "External HTC (W/m²·K)", DEFAULT_HTC_EXT, 0.1
                    ),
                    _num(
                        "input-htc-int", "Internal HTC (W/m²·K)", DEFAULT_HTC_INT, 0.1
                    ),
                    _num("input-tube-len", "Tube Length (m)", DEFAULT_TUBE_LEN, 0.01),
                    _num(
                        "input-tube-diam-ext",
                        "Tube Outer Diameter (m)",
                        DEFAULT_TUBE_DIAM_EXT,
                        0.001,
                    ),
                    _num(
                        "input-tube-thk", "Tube Thickness (m)", DEFAULT_TUBE_THK, 0.0001
                    ),
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
        
        return inputs
    
    def _generate_outputs(self):
        output = dbc.Card(
        [
            dbc.CardHeader(html.H5("Heat Duty Q")),
            dbc.CardBody(html.H2(id="output-q", className="text-primary my-0")),
        ],
        className="shadow-sm",
    )
        return output
    
    def _build_app(self, inputs, output):
        applet = dbc.Container(
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
        return applet

def build_layout_manager() -> dbc.Container:
    """Construct page layout (pure function)."""

    lmt = LMTD()
    inputs = lmt._generate_inputs()
    output = lmt._generate_outputs()
    applet = lmt._build_app(inputs, output)
    
    return applet
