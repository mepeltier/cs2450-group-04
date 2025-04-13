"""UVSim main entry point"""

from . import gui
import argparse
import textwrap
from .boot import Bootstrapper

boot = Bootstrapper()
mem = boot.memory
cpu = boot.cpu

parser = argparse.ArgumentParser(prog="UVSim", 
                                 formatter_class=argparse.RawDescriptionHelpFormatter, 
                                 add_help=False,
                                 usage="poetry run python src/main.py [file_path] [-h] [-v] [--version]",
                                 description=textwrap.dedent('''                        
                                    This project is managed with Poetry. In order to run this project, first install Poetry, through 'pip install poetry' or one of the recommended methods described by its documentation. 
                                    Once Poetry is installed, see the following commands:
                                    $ poetry lock -- This step shouldn't be necessary, but it will make sure that the lockfile is up to date with the latest versions.
                                                             
                                    $ poetry install --all-extras -- This creates a .venv/ folder, in which poetry installs all the necessary libraries to run this project.

                                    $ poetry run python src/main.py [file_path] [-h] [-v] [--version]

                                                             
                                    UVSim - Run a BasicML program
                                    --------------------------------              
                                    '''))

parser.add_argument("file", type=str, action="store", nargs="?", metavar = "file_path", default = None, help="file path to the BasicML input file")
parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose mode for debugging")
parser.add_argument("--version", action="version", version="%(prog)s 2.0")
parser.add_argument("-h", "--help", action="help", help="show this help message and exit", )
args = parser.parse_args()

def main():
    if args.file:
        try:
            open(args.file, "r")
        except FileNotFoundError:
            print(f"Error: File {args.file} not found.")
            return
        gui.App(boot, args.file)    
    else:
        gui.App(boot)

if __name__ == "__main__":
    if args.verbose:
        cpu.log = True
        mem.log = True
    main()
