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

        return data


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

        assert(len(self.split_line) >= 3 or len(self.split_line) <= 6)

        self.num_values = int(self.split_line[0])
        self.lower = int(self.split_line[1])
        self.upper = int(self.split_line[2])

        self.x_key = "x0"
        self.y_key = "y0"

        self.x_prefix = "Value"

        if len(self.split_line) > 3:
            self.x_key = str(self.split_line[3])

        if len(self.split_line) > 4:
            self.y_key = str(self.split_line[4])

        if len(self.split_line) > 5:
            self.x_prefix = str(self.split_line[5])

    def process(self, data: List[Dict]):
        for i in range(0, self.num_values):
            data.append({self.x_key: f"{self.x_prefix} {i + 1}", self.y_key: random.randint(self.lower, self.upper)})
            
        return data


@dataclass
class ListInjectRandInt(Instruction):
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
    ("list", "appendrandint"):      ListAppendRandInt,
    ("list", "injectrandint"):      ListInjectRandInt,
    ("item", "addint"):             ItemAddInt,
    # item addfromoffset (add value in y to value in y from index - 1 and store in y1)
}


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

                instruction = ISA.get((split_line[0], split_line[1]), Instruction("NOOP"))(split_line[2])
                self.instructions.append(instruction)

    def process(self, data: List[Dict]) -> List[Dict]:
        for instruction in self.instructions:
            data = instruction.process(data)

        return data


def get_mods(paths: List[str]):
    mods = [Mod(path=path) for path in paths]
    return mods
                
