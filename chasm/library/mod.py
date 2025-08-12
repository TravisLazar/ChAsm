import random
from typing import List, Dict
from pydantic import BaseModel, Field
from dataclasses import dataclass, field


@dataclass
class Instruction:
    args: Dict

    class InstructionArguments(BaseModel):
        pass

    def __post_init__(self):
        self.parsed_args = self.InstructionArguments(**self.args)

    def process(self, data: List[Dict]) -> List[Dict]:
        return data


@dataclass
class AddInt(Instruction):
    """
    For every item in the list of data, add a specified integer value
    """
    class InstructionArguments(BaseModel):
        adder: int = Field(
            ...,
            description="Value to add at specified key of each element",
            examples="100, 155, 304, 455, ..."
        )

        key: str = Field(
            ...,
            description="The key of each data element to add {adder} into",
            examples="y, y1, y2, x1, s1, s2, ..."
        )

    def __post_init__(self):
        super().__post_init__()

    def process(self, data: List[Dict]):
        for datum in data:
            datum[self.parsed_args.key] = datum[self.parsed_args.key] + self.parsed_args.adder

        return data


@dataclass
class AppendRandInt(Instruction):
    """
    Append a series of random integers to the end of the data set
    """
    class InstructionArguments(BaseModel):
        num: int = Field(
            ...,
            description="Number of entries to append to the data list.",
            examples="10, 15, 30, 50, 100, ..."
        )

        low: int = Field(
            ...,
            description="The minimum value that can be randomly generated",
            examples="0, 100, 1000, 1553, ..."
        )

        high: int = Field(
            ...,
            description="The maximum value that can be randomly generated",
            examples="1000, 2304, 10, 55, ..."
        )

        xkey: str = Field(
            default = "x0",
            description="The category (x) key to use when writing new random values. The value written here will increment from 1 to N.",
            examples="x0, x1, cat, date, ..."
        )

        ykey: str = Field(
            default = "y0",
            description="The value (y) key to use when writing new random values. This will be the key at which the integer value is written.",
            examples="y, y1, num, count, ..."
        )

        xprefix: str = Field(
            default = "Value",
            description="The prefix to use when writing to the {xkey} field. Will be used as a prefix for every incrementing 1-based value.",
            examples="Value, Category, Entry, ..."
        )

    def __post_init__(self):
        super().__post_init__()

    def process(self, data: List[Dict]):
        for i in range(0, self.parsed_args.num):
            data.append(
                {
                    self.parsed_args.xkey: f"{self.parsed_args.xprefix} {i + 1}", 
                    self.parsed_args.ykey: random.randint(self.parsed_args.low, self.parsed_args.high)
                }
            )
            
        return data


@dataclass
class InjectRandInt(Instruction):
    """
    Inject a random integer into each item in the data set
    """
    class InstructionArguments(BaseModel):
        low: int = Field(
            ...,
            description="The minimum value that can be randomly generated",
            examples="0, 100, 1000, 1553, ..."
        )

        high: int = Field(
            ...,
            description="The maximum value that can be randomly generated",
            examples="1000, 2304, 10, 55, ..."
        )

        ykey: str = Field(
            ...,
            description="The value (y) key to use when writing new random values. This will be the key at which the integer value is written.",
            examples="y, y1, num, count, ..."
        )

    def __post_init__(self):
        super().__post_init__()

    def process(self, data: List[Dict]):
        for datum in data:
            datum[self.parsed_args.ykey] = random.randint(self.parsed_args.low, self.parsed_args.high)
        
        return data


ISA = {
    "appendrandint":        AppendRandInt,
    "injectrandint":        InjectRandInt,
    "addint":               AddInt,
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
                
                inst_name, inst_arg_str = stripped_line.split(None, 1)
                inst_args = self._parse_args(inst_arg_str)

                instruction = ISA.get(inst_name, Instruction({}))(inst_args)
                self.instructions.append(instruction)

    def process(self, data: List[Dict]) -> List[Dict]:
        for instruction in self.instructions:
            data = instruction.process(data)

        return data


def get_mods(paths: List[str]):
    mods = [Mod(path=path) for path in paths]
    return mods
                
