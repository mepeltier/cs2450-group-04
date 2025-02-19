"""UVSim main entry point"""

import gui
import argparse
import textwrap
from typing import List

try:
    from src.boot import Bootstrapper
except ImportError:
    from .boot import Bootstrapper

boot = Bootstrapper()
io = boot.io
mem = boot.memory
cpu = boot.cpu

parser = argparse.ArgumentParser(prog="UVSim", 
                                 formatter_class=argparse.RawDescriptionHelpFormatter, 
                                 add_help=False,
                                 usage="poetry run python src/main.py [file_path] [-c] [-h] [-v] [--version]",
                                 description=textwrap.dedent('''                        
                                    This project is managed with Poetry. In order to run this project, first install Poetry, through 'pip install poetry' or one of the recommended methods described by its documentation. 
                                    Once Poetry is installed, see the following commands:
                                    $ poetry lock -- This step shouldn't be necessary, but it will make sure that the lockfile is up to date with the latest versions.
                                                             
                                    $ poetry install --all-extras -- This creates a .venv/ folder, in which poetry installs all the necessary libraries to run this project.

                                    $ poetry run python src/main.py [file_path] [-c] [-h] [-v] [--version]

                                                             
                                    UVSim - Run a BasicML program
                                    --------------------------------              
                                    '''))

parser.add_argument("-c", "--cli", action="store_true", help="run the program in CLI mode")
parser.add_argument("file", type=str, action="store", nargs="?", metavar = "file_path", default = None, help="file path to the BasicML input file")
parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose mode for debugging")
parser.add_argument("--version", action="version", version="%(prog)s 2.0")
parser.add_argument("-h", "--help", action="help", help="show this help message and exit", )
args = parser.parse_args()

def main():
    if args.file:
        if io.read_from_file(args.file) != []:
            gui.App(boot, args.file)
    else:
        gui.App(boot)

def cli():
    io.write("\nWelcome to UVSim - BasicML Simulator")
    
    if args.file:
        boot.load_program(args.file)
        boot.run()
        return
    else:
        io.write("\n---Manual Instruction Input Mode---")
        program: List[str] = []

        while True:
            op = io.read_string("Enter a 4-digit signed instruction (type 'END' to finish): ")
            if op.upper() == "END":
                break
            
            try:
                mem.validate_word(op)
            except Exception as e:
                io.write(e, True)
                continue

            program.append(op)
        for addr, instruction in enumerate(program):
            try:
                mem.write(addr, instruction.split()[0].rstrip())
            except IndexError as e:
                io.write(e, True)
                return
            except ValueError as e:
                io.write(e, True)
                mem.write(addr, "+0000")
        if len(program) >= 1:
            boot.run()

if __name__ == "__main__":
    if args.verbose:
        cpu.log = True
        mem.log = True
        io.log = True
    
    if args.cli:
        cli()
    else:
        main()
