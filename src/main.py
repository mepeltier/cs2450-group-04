"""UVSim main entry point"""

import argparse
import textwrap
from typing import List
try:
    from src.boot import Bootstrapper
except ModuleNotFoundError:
    from .boot import Bootstrapper

boot = Bootstrapper()
io = boot.io
mem = boot.memory
cpu = boot.cpu

parser = argparse.ArgumentParser(prog="UVSim", 
                                 formatter_class=argparse.RawDescriptionHelpFormatter, 
                                 add_help=False,
                                 usage="poetry run python src/main.py [file_path | -m] [-h] [-v] [--version]",
                                 description=textwrap.dedent('''                        
                                    This project is managed with Poetry. In order to run this project, first install Poetry, through 'pip install poetry' or one of the recommended methods described by its documentation. 
                                    Once Poetry is installed, see the following commands:

                                    $ poetry lock -- This step shouldn't be necessary, but it will make sure that the lockfile is up to date with the latest versions.

                                    $ poetry install --all-extras -- This creates a .venv/ folder, in which poetry installs all the necessary libraries to run this project.
                                                             
                                    $ poetry run python src/main.py [file_path | -m] [-h] [-v] [--version]
                                                             
                                                             
                                    UVSim - Run a BasicML program
                                    --------------------------------              
                                    '''))
group = parser.add_mutually_exclusive_group()
group.add_argument("file", type=str, action="store", nargs="?", metavar = "file_path", default = None, help="file path to the BasicML input file")
group.add_argument("-m", "--manual", action="store_true", help="manually enter opcodes instead of reading from a file")
parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose mode for debugging")
parser.add_argument("--version", action="version", version="%(prog)s 1.0")
parser.add_argument("-h", "--help", action="help", help="show this help message and exit", )
args = parser.parse_args()

def main():
    io.write("\nWelcome to UVSim - Universal Virtual Simulator")

    if args.verbose:
        cpu.log = True
    
    if not args.file and not args.manual:
        file_path = io.read_string("Enter the file path to the BasicML input file (type 'manual' to start typing instructions):\n")
        if file_path.lower() == "manual":
            args.manual = True
        else:
            try:
                io.read_from_file(file_path)
            except FileNotFoundError as e:
                io.write(e, True)
                return
            boot.load_program(file_path)
            boot.run()
            return
    
    if args.manual and not args.file:
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
        if len(program) > 1:
            boot.run()
    elif args.file:
        boot.load_program(args.file)
        boot.run()
        return
    else:
        parser.print_help()
        exit(0)

if __name__ == "__main__":
    main()