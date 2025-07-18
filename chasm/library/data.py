import json
from typing import Any, List


def parse_data_input(data: Any) -> List[dict]:
    if isinstance(data, str):
        obj = json.loads(data)

        # TODO: Need to do loads of data management here for all sorts of scenarios
        return obj

    elif isinstance(data, List):
        pass 
