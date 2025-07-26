from typing import List
from dataclasses import dataclass, field


@dataclass
class ChartConfig:
    data_xkey: str =                    "x"
    data_ykey: str =                    "y"

    chart_title: str =                  "Hello Bar Chart"

    chart_margin_l: int =               None
    chart_margin_r: int =               None
    chart_margin_t: int =               None
    chart_margin_b: int =               None
    chart_automargin: bool =            True

    chart_paper_bgcolor: str =          '#ffffff'
    chart_plot_bgcolor: str =           '#ffffff'
    chart_colorway: List[str] =         field(
                                            default_factory=lambda: [
                                                "#1d95dd",
                                                "#2ab2a5",
                                                "#e82e5d",
                                                "#011627",
                                            ]
                                        )

    chart_xaxis_title: str =            "x-Title"
    chart_xaxis_visible: bool =         True
    chart_xaxis_showticklabels: bool =  True
    chart_xaxis_showgrid: bool =        True
    chart_xaxis_zeroline: bool =        True

    chart_yaxis_title: str =            "y-Title"
    chart_yaxis_visible: bool =         True
    chart_yaxis_showticklabels: bool =  True
    chart_yaxis_showgrid: bool =        True
    chart_yaxis_zeroline: bool =        True

    marker_line_width: int =            0

    def apply_layer(self, obj: dict) -> None:
        for key, value in obj.items():
            if hasattr(self, key):
                setattr(self, key, value)