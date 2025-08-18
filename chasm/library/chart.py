import plotly.graph_objects as go
from plotly.subplots import make_subplots

from typing import Any, List

from chasm.library.data import parse_data_input
from chasm.library.layer import get_chart_config
from chasm.library.config import ChartConfig


def make_chart(chart_type: str, raw_data: Any, layer_paths: List[str], mod_paths: List[str], output_path: str) -> go.Figure:
    data = parse_data_input(raw_data, mod_paths)
    config = get_chart_config(data=data, layers=layer_paths)

    # Bar Type Chart
    if chart_type in ("bar", "stackedbar"):
        if chart_type == "stackedbar":
            config.chart_layout_barmode = "stack"
            
        return make_bar(data, config, output_path)
    
    # Scatter Type Charts
    if chart_type in ("scatter", "scatter+line", "line"):
        config.scatter_mode = "markers"

        if chart_type == "line":
            config.scatter_mode = "lines"

        elif chart_type == "scatter+line":
            config.scatter_mode = "lines+markers"

        return make_scatter(data, config, output_path)


def make_figure(config: ChartConfig) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.update_layout(
        title_text=config.chart_title_text,
        title_font_weight=config.chart_title_font_weight,
        title_font_size=config.chart_title_font_size,
        title_pad=dict(
            l=config.chart_title_pad_l,
            r=config.chart_title_pad_r,
            t=config.chart_title_pad_t,
            b=config.chart_title_pad_b
        ),
        title_automargin=config.chart_title_automargin,
        paper_bgcolor=config.chart_paper_bgcolor,
        plot_bgcolor=config.chart_plot_bgcolor,
        colorway=config.chart_colorway,
        barmode=config.chart_layout_barmode,
        showlegend=config.chart_layout_showlegend,
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
        zeroline=config.chart_xaxis_zeroline,
        automargin=config.chart_xaxis_automargin,
        gridcolor=config.chart_xaxis_gridcolor,
        ticklabelstandoff=config.chart_yaxis_ticklabelstandoff
    )

    fig.update_yaxes(
        title=config.chart_yaxis_title,
        visible=config.chart_yaxis_visible,
        showticklabels=config.chart_yaxis_showticklabels,
        showgrid=config.chart_yaxis_showgrid,
        zeroline=config.chart_yaxis_zeroline,
        automargin=config.chart_yaxis_automargin,
        gridcolor=config.chart_yaxis_gridcolor,
        ticklabelstandoff=config.chart_yaxis_ticklabelstandoff
    )

    return fig


def make_scatter(data: List[dict], config: ChartConfig, output_path: str) -> go.Figure:
    fig = make_figure(config)

    for idx, y_key in enumerate(config.data_ykeys):
        x_key = config.data_xkey

        orientation = config.orientation

        if orientation == 'v':
            x_data = [d[x_key] for d in data]
            y_data = [d[y_key] for d in data]
        elif orientation == 'h':
            y_data = [d[x_key] for d in data]
            x_data = [d[y_key] for d in data]

        if y_key in config.data_ykeys:
            trace = go.Scatter(
                x=x_data, 
                y=y_data, 
                marker_line_width=config.marker_line_width, 
                mode=config.get_config(y_key, "scatter_mode"), 
                orientation=config.get_config(y_key, "orientation"),
                name=config.data_ykey_name_lookup.get(y_key, f"Series {y_key}") 
            )

            fig.add_trace(trace, secondary_y=False)

    # TODO: Move out of this function
    fig.write_image(f"{output_path}")

    return fig


def make_bar(data: List[dict], config: ChartConfig, output_path: str) -> go.Figure:
    fig = make_figure(config)

    for idx, y_key in enumerate(config.data_ykeys + config.data_skeys):
        x_key = config.data_xkey

        orientation = config.orientation

        if orientation == 'v':
            x_data = [d[x_key] for d in data]
            y_data = [d[y_key] for d in data]
        elif orientation == 'h':
            y_data = [d[x_key] for d in data]
            x_data = [d[y_key] for d in data]

        if y_key in config.data_ykeys:
            trace = go.Bar(
                x=x_data, 
                y=y_data,
                marker_line_width=config.marker_line_width,
                orientation=orientation,
                name=config.data_ykey_name_lookup.get(y_key, f"Series {y_key}")
            )

            fig.add_trace(trace, secondary_y=False)

        elif y_key in config.data_skeys:
            trace = go.Scatter(
                x=x_data, 
                y=y_data,
                marker_line_width=config.marker_line_width,
                orientation=orientation,
                name=config.data_ykey_name_lookup.get(y_key, f"Series {y_key}")
            )

            fig.add_trace(trace, secondary_y=True)

    # TODO: Move out of this function
    fig.write_image(f"{output_path}")

    return fig