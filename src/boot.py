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

    def load_program(self, file_name: str):
        """Load a program into memory starting at address 0.

        Parameters:
        program (list): List of strings representing BasicML instructions

        Raises:
        ValueError: If program is too large for memory
        """
        with open(file_name, "r") as file:
            program: List[str] = []

            for line in file.readlines():
                program.append(line)

            for addr, instruction in enumerate(program):
                try:

                    self.memory.write(addr, instruction.split()[0].rstrip())

                except IndexError as error:
                    LOGGER.error(
                        "Invalid index when loading program: \n%s", error.__str__()
                    )
                    return

                except ValueError as error:
                    LOGGER.error(
                        "Invalid instruction in file: %s\n%s\n\n"
                        "Zeroing out register %s",
                        addr,
                        instruction,
                        error.__str__(),
                    )
                    self.memory.write(addr, "+0000")

    def run(self, gui, cont=False):
        """Run the CPU."""
        self.cpu.run(gui, cont)
