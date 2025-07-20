import os, json
from typing import Any, List, Dict
from chasm.library.mod import Mod, get_mods


def parse_data_input_string(input_string: str) -> List[Dict[str, Any]]:
    """
    Parse a JSON string or file into a list of dictionary objects.
    
    Args:
        input_string: Either a file path or a JSON string representation
        
    Returns:
        List of dictionary objects
        
    Raises:
        FileNotFoundError: If the file path doesn't exist
        json.JSONDecodeError: If the JSON is invalid
        ValueError: If JSON is not a list of dictionaries or keys don't match
    """
    data = None
    
    # Check if the input string provided points at a valid path
    if os.path.isfile(input_string):
        try:
            with open(input_string, 'r', encoding='utf-8') as file:
                data = json.load(file)

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {input_string}")
        
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in file {input_string}: {e.msg}", e.doc, e.pos)
    else:
        # If it's not a path then we assume it's a JSON string
        try:
            data = json.loads(input_string)

        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON string: {e.msg}", e.doc, e.pos)
    
    # Once we load the data, it must be a list
    if not isinstance(data, list):
        raise ValueError("JSON must be a list")
    
    # Check if list is empty
    if len(data) == 0:
        return []
    
    # Further, the list must contain only dictionary elements
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {i} is not a dictionary")
    
    # We expect the data to be uniform, where ever element contains the same
    # keys. This may be something we change in the future, but for now we
    # assume uniform data structures.
    if len(data) > 0:
        first_keys = set(data[0].keys())

        for i, item in enumerate(data[1:], 1):
            current_keys = set(item.keys())
            
            if current_keys != first_keys:
                raise ValueError(f"Dictionary at index {i} has different keys. "
                               f"Expected: {sorted(first_keys)}, "
                               f"Got: {sorted(current_keys)}")
    
    return data


def parse_data_input(data: Any, mod_paths: List[Mod]) -> List[dict]:
    data_list = parse_data_input_string(data)

    # Put through modulators
    mods = get_mods(mod_paths)

    for mod in mods:
        mod.process(data_list)

    return data_list
