"""Class to parse a BasicML file into Memory."""

import logging
from typing import List
from src.cpu import CPU
from src.memory import Memory

LOGGER = logging.getLogger(__name__)


class Bootstrapper:
    """Class to bootstrap the UVSim module.

    Parse a file containing BasicML instructions and load it into memory.
    """

    def __init__(self) -> None:
        """Boostrap CPU, Memory, IOHandler."""
        self.memory = Memory()
        self.cpu = CPU(self.memory)

    def run(self, gui, cont=False):
        """Run the CPU."""
        self.cpu.run(gui, cont)
