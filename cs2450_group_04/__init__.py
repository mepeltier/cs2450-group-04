from typing import Dict
from instruction_set import (
    Instruction,
    Read,
    Write,
    Load,
    Store,
    Add,
    Subtract,
    Multiply,
    Divide,
    Branch,
    BranchNeg,
    BranchZero,
    Halt,
)

INSTRUCTIONS: Dict[int, Instruction.__class__] = {
    Read.opcode: Read,
    Write.opcode: Write,
    Load.opcode: Load,
    Store.opcode: Store,
    Add.opcode: Add,
    Subtract.opcode: Subtract,
    Multiply.opcode: Multiply,
    Divide.opcode: Divide,
    Branch.opcode: Branch,
    BranchNeg.opcode: BranchNeg,
    BranchZero.opcode: BranchZero,
    Halt.opcode: Halt,
}
