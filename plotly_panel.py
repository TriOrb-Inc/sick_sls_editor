from __future__ import annotations

import plotly.graph_objs as go


def build_sample_figure() -> go.Figure:
    """Return an empty Plotly figure with axis/grid styling."""

    fig = go.Figure(data=[])

    axis_style = dict(
        showgrid=True,
        gridcolor="#d9dee7",
        gridwidth=1,
        zeroline=True,
        zerolinecolor="#9fb3d1",
        zerolinewidth=2,
        showline=True,
        linewidth=2,
        linecolor="#6b7a99",
        range=[-1000, 1000],
        constrain="range",
        tick0=0,
        dtick=100,
        minor=dict(showgrid=True, gridcolor="#f2f5fb", gridwidth=0.5, dtick=50),
    )
    fig.update_xaxes(title="X[mm]", **axis_style)
    fig.update_yaxes(title="Y[mm]", scaleanchor="x", scaleratio=1, **axis_style)
    helper_lines = []
    for value in (-750, -500, -250, 250, 500, 750):
        helper_lines.append(
            dict(
                type="line",
                xref="x",
                yref="y",
                x0=-1000,
                x1=1000,
                y0=value,
                y1=value,
                line=dict(color="#cbd5f5", width=1, dash="dot"),
            )
        )
        helper_lines.append(
            dict(
                type="line",
                xref="x",
                yref="y",
                x0=value,
                x1=value,
                y0=-1000,
                y1=1000,
                line=dict(color="#cbd5f5", width=1, dash="dot"),
            )
        )
    fig.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=60, r=20, t=30, b=60),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        shapes=helper_lines,
    )

    return fig
