import re
from typing import List, Dict
from dataclasses import dataclass, field


# TODO: Explore pydantic for this class (for many reasons)
@dataclass
class ChartConfig:
    data_xkey: str =                    "x"

    data_ykey_match: str =              r"^y\d*$"
    data_ykeys: List[str] =             None # If None, computed at runtime from ykey_match

    data_ykey_name_lookup: Dict[str, str] = field(default_factory=dict)

    data_skey_match: str =              r"^s\d*$"
    data_skeys: List[str] =             None # If None, computed at runtime from skey_match

    data_skey_name_lookup: Dict[str, str] = field(default_factory=dict)

    data_yskey_match: str =             r"^ys\d*$"
    data_yskeys: List[str] =            None # If None, computed at runtime from yskey_match

    data_yskey_name_lookup: Dict[str, str] = field(default_factory=dict)

    chart_layout_barmode: str =         "group"
    chart_layout_showlegend: bool =     False

    chart_title_text: str =             None
    chart_title_font_weight: int =      650
    chart_title_font_size: int =        20
    chart_title_pad_l: int =            8
    chart_title_pad_r: int =            8
    chart_title_pad_t: int =            8
    chart_title_pad_b: int =            8
    chart_title_automargin: bool =      True

    chart_margin_l: int =               35
    chart_margin_r: int =               15
    chart_margin_t: int =               15
    chart_margin_b: int =               35
    chart_automargin: bool =            True

    chart_paper_bgcolor: str =          "#ffffff"
    chart_plot_bgcolor: str =           "#ffffff"
    chart_colorway: List[str] =         field(
                                            default_factory=lambda: [
                                                "#1d95dd",
                                                "#2ab2a5",
                                                "#e82e5d",
                                                "#011627",
                                            ]
                                        )

    chart_xaxis_title: str =            None
    chart_xaxis_visible: bool =         True
    chart_xaxis_showticklabels: bool =  True
    chart_xaxis_showgrid: bool =        False
    chart_xaxis_zeroline: bool =        True
    chart_xaxis_automargin: bool =      True
    chart_xaxis_gridcolor: str =        "#d3dbdc"
    chart_xaxis_ticklabelstandoff: int = 7

    chart_yaxis_title: str =            None
    chart_yaxis_visible: bool =         True
    chart_yaxis_showticklabels: bool =  True
    chart_yaxis_showgrid: bool =        True
    chart_yaxis_zeroline: bool =        True
    chart_yaxis_automargin: bool =      True
    chart_yaxis_gridcolor: str =        "#d3dbdc"
    chart_yaxis_ticklabelstandoff: int = 7

    marker_line_width: int =            0

    scatter_mode: str =                 "markers"

    orientation: str =                  "v"

    #
    # Index Specific Configs
    #   Anything inside of this dictionary will override specific settings for specific keys.
    #   This allows different series of the chart to have different config options, such as 
    #   a line chart where one of the series is markers only and one is markers+lines.
    #
    #   Example Structure:
    #       y0: 
    #           scatter_mode: markers
    #       y1:
    #           scatter_mode: markers+lines
    #  
    isc: Dict[str, Dict[str, str]] =    field(default_factory=dict)

    def get_config(self, key, setting_name):
        # Handle ISCs
        if key in self.isc and setting_name in self.isc[key]:
            return self.isc[key][setting_name]
        
        return getattr(self, setting_name)

    def apply_layer(self, obj: Dict) -> None:
        for key, value in obj.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def _compute_keys_from_match(self, data_sample: Dict, matcher: str) -> List[str]:
        return [key for key in data_sample.keys() if re.fullmatch(matcher, key)]

    def compute_keys(self, data_sample):
        if not self.data_ykeys:
            self.data_ykeys = self._compute_keys_from_match(data_sample, self.data_ykey_match)

        if not self.data_skeys:
            self.data_skeys = self._compute_keys_from_match(data_sample, self.data_skey_match)

        if not self.data_yskeys:
            self.data_yskeys = self._compute_keys_from_match(data_sample, self.data_yskey_match)
