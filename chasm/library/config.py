from dataclasses import dataclass


@dataclass
class ChartConfig:
    data_xkey: str =                    "x"
    data_ykey: str =                    "y"

    chart_title: str =                  "Hello Bar Chart"
    chart_margin_l: int =               5
    chart_margin_r: int =               5
    chart_margin_t: int =               5
    chart_margin_b: int =               5
    chart_paper_bgcolor: str =          '#ffffff'
    chart_plot_bgcolor: str =           '#ffffff'

    chart_xaxis_title: str =            "x-Title"
    chart_xaxis_visible: bool =         True
    chart_xaxis_showticklabels =        True
    chart_xaxis_showgrid: bool =        True
    chart_xaxis_zeroline: bool =        True

    chart_yaxis_title: str =            "y-Title"
    chart_yaxis_visible: bool =         True
    chart_yaxis_showticklabels: bool =  True
    chart_yaxis_showgrid: bool =        True
    chart_yaxis_zeroline: bool =        True

    def apply_layer(self, obj: dict) -> None:
        for key, value in obj.items():
            if hasattr(self, key):
                setattr(self, key, value)