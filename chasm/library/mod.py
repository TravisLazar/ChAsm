import random
from typing import List, Dict
from dataclasses import dataclass, field


@dataclass
class Instruction:
    line: str

    def __post_init__(self):
        self.split_line = self.line.split(",")
        self.split_line = [line.strip() for line in self.split_line]

    def process(self, data: List[Dict]) -> List[Dict]:
        return data


@dataclass
class ItemAddInt(Instruction):
    """
    For every item in the list of data, add a specified integer value

    type:           item
    instruction:    addint

    params:     
        value       <int> value to add to each item
        key         <str> key to modify in the data set
    """
    def __post_init__(self):
        super().__post_init__()

        assert(len(self.split_line) == 2)

        self.adder = int(self.split_line[0])
        self.key = str(self.split_line[1])

    def process(self, data: List[Dict]):
        for datum in data:
            datum[self.key] = datum[self.key] + self.adder


@dataclass
class ListAppendRandInt(Instruction):
    """
    Append a series of random integers to the end of the data set

    type:           list
    instruction:    appendrandint

    params:     
        num         <int> Number of values to append
        lower       <int> Lower bound (inclusive) for random number generation
        upper       <int> Upper bound (inclusive) for random number generation
    """
    def __post_init__(self):
        super().__post_init__()

        assert(len(self.split_line) == 3)

        self.num_values = int(self.split_line[0])
        self.lower = int(self.split_line[1])
        self.upper = int(self.split_line[2])

    def process(self, data: List[Dict]):
        for i in range(0, self.upper):
            data.append({"x": f"Value {i + 1}", "y": random.randint(self.lower, self.upper)})
            
        return data


@dataclass
class Mod:
    path: str
    instructions: List[Instruction] = field(default_factory=list)

    def __post_init__(self):
        with open(self.path, 'r') as file:
            for line in file:
                stripped_line = line.strip()

                if stripped_line.startswith("#"):
                    continue
                elif not stripped_line:
                    continue
                
                # TODO: This is so error prone it's crazy, come back and add good sanitization
                split_line = stripped_line.split(None, 2)

                assert(len(split_line) == 3)

                if split_line[0] == "list":
                    if split_line[1] == "appendrandint":
                        self.instructions.append(ListAppendRandInt(line=split_line[2]))

                elif split_line[0] == "item":
                    if split_line[1] == "addint":
                        self.instructions.append(ItemAddInt(line=split_line[2]))

    def process(self, data: List[Dict]) -> List[Dict]:
        for instruction in self.instructions:
            data = instruction.process(data)

        return data


def get_mods(paths: List[str]):
    mods = [Mod(path=path) for path in paths]
    return mods
                
