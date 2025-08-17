import yaml
import os
from chasm.library.config import ChartConfig

def get_layer_obj(path) -> dict:
    # Check if the input string provided points at a valid path
    if os.path.isfile(path):
        try:
            with open(path, 'r') as file:
                data = yaml.safe_load(file)
                return data

        except FileNotFoundError:
            print(f"Error: The file '{path}' was not found.")
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML: {exc}")

    else:
        try:
            data = yaml.safe_load(path)
            return data

        except yaml.YAMLError as exc:
            print(f"Error parsing YAML: {exc}")


def get_chart_config(data, layers) -> ChartConfig:
    config = ChartConfig()

    for layer in layers:
        obj = get_layer_obj(layer)
        config.apply_layer(obj)

    # TODO: Should this go into the apply_layer function? It will reduce performance
    # but all reduce the chance that this gets missed in other future logic.
    config.compute_keys(data[0])

    return config