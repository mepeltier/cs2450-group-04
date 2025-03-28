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

    def load_program(self, program):
        """Load a program from a list of instructions into memory, starting at address 0
        
        Parameters:
        program (list): List of strings representing BasicML instructions

        Raises:
        ValueError: If program is too large for memory
        IndexError: If address is invalid
        """
        try:
            for addr, instruction in enumerate(program):                
                self.memory.write(addr, instruction.split()[0].rstrip())
        except IndexError:
            raise IndexError(addr)
        except ValueError:
            raise ValueError(instruction)
                               

    def load_from_file(self, file_name: str):
        """Create a list of instructions from reading a file to pass to load_program()

        Parameters:
        file_name (str) : file_name location

        Raises:
        ValueError: If program is too large for memory
        """
        with open(file_name, "r") as file:
            program: List[str] = []

            for line in file.readlines():
                words = line.split()
                program.append(words[0])

            self.load_program(program)

    def run(self, gui, cont=False):
        """Run the CPU."""
        self.cpu.run(gui, cont)


def main():
    boot = Bootstrapper()

    boot.load_from_file("tests/cpu_test_6digit.txt")
    print(boot.cpu.print_memory())

if __name__ == "__main__":
    main()