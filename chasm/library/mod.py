import random
from typing import List, Dict
from pydantic import BaseModel
from dataclasses import dataclass, field


@dataclass
class Instruction:
    args: Dict

    class InstructionArguments(BaseModel):
        pass

    def _typecheck(self):
        return self.InstructionArguments(**self.args)

    def __post_init__(self):
        self.parsed_args = self._typecheck()

    def process(self, data: List[Dict]) -> List[Dict]:
        return data


@dataclass
class ItemAddInt(Instruction):
    """
    For every item in the list of data, add a specified integer value
    """
    def __post_init__(self):
        super().__post_init__()

        assert(len(self.split_line) == 2)

        self.adder = int(self.split_line[0])
        self.key = str(self.split_line[1])

    def process(self, data: List[Dict]):
        for datum in data:
            datum[self.key] = datum[self.key] + self.adder

        return data


@dataclass
class AppendRandInt(Instruction):
    """
    Append a series of random integers to the end of the data set
    """
    class InstructionArguments(BaseModel):
        num: int
        low: int
        high: int
        xkey: str = "x0"
        ykey: str = "y0"
        xprefix: str = "Value"

    def __post_init__(self):
        super().__post_init__()

    def process(self, data: List[Dict]):
        for i in range(0, self.parsed_args.num):
            data.append({self.parsed_args.xkey: f"{self.parsed_args.xprefix} {i + 1}", self.parsed_args.ykey: random.randint(self.parsed_args.low, self.parsed_args.high)})
            
        return data


@dataclass
class ItemInjectRandInt(Instruction):
    """
    Inject a random integer into each item in the data set

    type:           list
    instruction:    injectrandint

    params:     
        num         <int> Number of values to append
        lower       <int> Lower bound (inclusive) for random number generation
        upper       <int> Upper bound (inclusive) for random number generation
    """
    def __post_init__(self):
        super().__post_init__()

        assert(len(self.split_line) == 3)

        self.lower = int(self.split_line[0])
        self.upper = int(self.split_line[1])
        self.y_key = str(self.split_line[2])

    def process(self, data: List[Dict]):
        for datum in data:
            datum[self.y_key] = random.randint(self.lower, self.upper)
            
        return data


ISA = {
    "appendrandint":        AppendRandInt,
    "injectrandint":        ItemInjectRandInt,
    "addint":               ItemAddInt,
}


@dataclass
class Mod:
    path: str
    instructions: List[Instruction] = field(default_factory=list)

    def _parse_args(self, arg_string) -> Dict:
        """Parse a line with best type guesses"""

        result = {}

        # Split by comma and strip whitespace
        pairs = [pair.strip() for pair in arg_string.split(',')]
        
        for pair in pairs:
            if '=' not in pair:
                raise ValueError(f"ChAsm instruction pair {pair} is malformed in some way.")
            
            key, value = pair.split('=', 1)  # Split only on first '='
            key = key.strip()
            value = value.strip()
            
            # Smart type conversion
            if value.lower() in ('true', 'false'):
                result[key] = value.lower() == 'true'
            elif value.lower() in ('null', 'none'):
                result[key] = None
            else:
                try:
                    # Try int first, then float
                    if '.' in value:
                        result[key] = float(value)
                    else:
                        result[key] = int(value)
                except ValueError:
                    result[key] = value  # Keep as string
        
        return result

    def __post_init__(self):
        with open(self.path, 'r') as file:
            for line in file:
                stripped_line = line.strip()

                if stripped_line.startswith("#"):
                    continue
                elif not stripped_line:
                    continue
                
                # TODO: This is so error prone it's crazy, come back and add good sanitization
                inst_name, inst_arg_str = stripped_line.split(None, 1)
                inst_args = self._parse_args(inst_arg_str)

                # Validate with pydantic and pass model to instruction???

                # assert(len(split_line) == 2)

                instruction = ISA.get(inst_name, Instruction({}))(inst_args)
                self.instructions.append(instruction)

    def process(self, data: List[Dict]) -> List[Dict]:
        for instruction in self.instructions:
            data = instruction.process(data)

        return data


def get_mods(paths: List[str]):
    mods = [Mod(path=path) for path in paths]
    return mods
                
