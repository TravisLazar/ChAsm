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

    trace = go.Bar(x=xs, y=ys)
    fig = go.Figure(trace)

    fig.update_layout(
        title=config.chart_title,
    )

    fig.update_xaxes(
        title=config.chart_xaxis_title,
        visible=config.chart_xaxis_visible
    )

    fig.update_yaxes(
        title=config.chart_yaxis_title,
        visible=config.chart_yaxis_visible
    )
    
    # TODO: Move out of this function
    fig.write_image(f"{output_folder}/hello_world.svg")

    return fig