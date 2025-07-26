import plotly.graph_objects as go

from typing import Any, List

from chasm.library.data import parse_data_input
from chasm.library.layer import get_chart_config
from chasm.library.config import ChartConfig


def make_chart(chart_type: str, raw_data: Any, layer_paths: List[str], mod_paths: List[str], output_folder: str) -> go.Figure:
    data = parse_data_input(raw_data, mod_paths)
    config = get_chart_config(layers=layer_paths)

    if chart_type == "bar":
        return make_bar(data, config, output_folder)


def make_bar(data: List[dict], config: ChartConfig, output_folder: str) -> go.Figure:
    xs = [d[config.data_xkey] for d in data]
    ys = [d[config.data_ykey] for d in data]

    trace = go.Bar(
        x=xs, 
        y=ys,
        marker_line_width=config.marker_line_width
    )
    
    fig = go.Figure(trace)

    fig.update_layout(
        title=config.chart_title,
        paper_bgcolor=config.chart_paper_bgcolor,
        plot_bgcolor=config.chart_plot_bgcolor,
        colorway=config.chart_colorway,
        margin=dict(
            l=config.chart_margin_l,
            r=config.chart_margin_r,
            t=config.chart_margin_t,
            b=config.chart_margin_b
        )
    )

    fig.update_xaxes(
        title=config.chart_xaxis_title,
        visible=config.chart_xaxis_visible,
        showticklabels=config.chart_xaxis_showticklabels,
        showgrid=config.chart_xaxis_showgrid,
        zeroline=config.chart_xaxis_zeroline
    )

    fig.update_yaxes(
        title=config.chart_yaxis_title,
        visible=config.chart_yaxis_visible,
        showticklabels=config.chart_yaxis_showticklabels,
        showgrid=config.chart_yaxis_showgrid,
        zeroline=config.chart_yaxis_zeroline
    )
    
    # TODO: Move out of this function
    fig.write_image(f"{output_folder}/hello_world.svg")

    return fig