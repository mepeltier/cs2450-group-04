"""Instruction set for BasicML."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class InstructionSet(Enum):

    # I/O Operations
    READ = 10
    WRITE = 11

    # Load/store
    LOAD = 20
    STORE = 21

    # Arithmetic methods
    ADD = 30
    SUBTRACT = 31
    DIVIDE = 32
    MULTIPLY = 33

    # Control operations
    BRANCH = 40
    BRANCHNEG = 41
    BRANCHZERO = 42
    HALT = 43


# Python doesn't really do interfaces; ABCs are the closest we get,
# but I thought this would be a good way to do make sure instructions are extendable
class Instruction(ABC):
    name: str
    opcode: int

    def __init__(
        self,
        address: Optional[int] = None,
    ) -> None:
        self.address = address

    @abstractmethod
    def call_instruction(self):
        pass


class Read(Instruction):
    name = "READ"
    opcode = 10

    def __init__(self, address) -> None:
        super().__init__(address)

    def call_instruction(self):
        """Read a word from the keyboard into a specific locaiton in memory."""


class Write(Instruction):
    name = "WRITE"
    opcode = 11

    def __init__(self, address) -> None:
        super().__init__(address)

    def call_instruction(self):
        """Write a word from a specific location in memory to screen."""


class Load(Instruction):
    name = "LOAD"
    opcode = 20

    def __init__(self, address) -> None:
        super().__init__(address)

    def call_instruction(self):
        """Load a word from a specific location in memory into the accumulator."""


class Store(Instruction):
    name = "STORE"
    opcode = 21

    def __init__(self, address) -> None:
        super().__init__(address)

    def call_instruction(self):
        """Store a word from the accumulator into a specific locaiton in memory."""


class Add(Instruction):
    name = "ADD"
    opcode = 30

    def __init__(self, address) -> None:
        super().__init__(address)

    def call_instruction(self):
        """Add a word from a specific location in memory to the word in the accumulator.

        (leave the result in the accumulator)
        """


class Subtract(Instruction):
    name = "SUBTRACT"
    opcode = 31

    def __init__(self, address) -> None:
        super().__init__(address)

    def call_instruction(self):
        """Subtract a word from a location in memory from the word in the accumulator.

        (leave the result in the accumulator)
        """


class Divide(Instruction):
    name = "DIVIDE"
    opcode = 32

    def __init__(self, address) -> None:
        super().__init__(address)

    def call_instruction(self):
        """Divide the word in the accumulator by a word from a location in memory.

        (leave the result in the accumulator).
        """


class Multiply(Instruction):
    name = "MULTIPLY"
    opcode = 33

    def __init__(self, address) -> None:
        super().__init__(address)

    def call_instruction(self):
        """Multiply the word in the accumulator by a word from a location in memory.

        (leave the result in the accumulator).
        """


class Branch(Instruction):
    name = "BRANCH"
    opcode = 40

    def __init__(self, address) -> None:
        super().__init__(address)

    def call_instruction(self):
        """Branch to a specific location in memory."""


class BranchNeg(Instruction):
    name = "BRANCHNEG"
    opcode = 41

    def __init__(self, address) -> None:
        super().__init__(address)

    def call_instruction(self):
        """Branch to a specific location in memory if the accumulator is negative."""


class BranchZero(Instruction):
    name = "BRANCHZERO"
    opcode = 42

    def __init__(self, address) -> None:
        super().__init__(address)

    def call_instruction(self):
        """Branch to a specific location in memory if the accumulator is zero."""


class Halt(Instruction):
    name = "READ"
    opcode = 43

    def call_instruction(self):
        """Pause the program."""
