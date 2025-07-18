import yaml
from chasm.library.config import ChartConfig

def get_layer_obj(path) -> dict:
    try:
        with open(path, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML: {exc}")


def get_chart_config(layers) -> ChartConfig:
    config = ChartConfig()

    for layer in layers:
        obj = get_layer_obj(layer)
        config.apply_layer(obj)

    return config