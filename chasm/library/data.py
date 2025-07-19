import json
from typing import Any, List
from chasm.library.mod import Mod, get_mods


def parse_data_input(data: Any, mod_paths: List[Mod]) -> List[dict]:
    data_list = None

    if isinstance(data, str):
        data_list = json.loads(data)
        # TODO: Need to do loads of data management here for all sorts of scenarios

    elif isinstance(data, List):
        pass 

    # Put through modulators
    mods = get_mods(mod_paths)

    for mod in mods:
        mod.process(data_list)

    return data_list
