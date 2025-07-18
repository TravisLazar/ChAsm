from dataclasses import dataclass


@dataclass
class ChartConfig:
    data_xkey: str =                "x"
    data_ykey: str =                "y"

    chart_title: str =              "Hello Bar Chart"

    chart_xaxis_title: str =        "x-Title"
    chart_xaxis_visible: bool =     True

    chart_yaxis_title: str =        "y-Title"
    chart_yaxis_visible: bool =     True

    def apply_layer(self, obj: dict) -> None:
        for key, value in obj.items():
            if hasattr(self, key):
                setattr(self, key, value)