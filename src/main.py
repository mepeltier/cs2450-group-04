"""UVSim main entry point"""

import argparse
from typing import List
from src.boot import Bootstrapper

boot = Bootstrapper()
io = boot.io
mem = boot.memory
cpu = boot.cpu

parser = argparse.ArgumentParser(prog="UVSim", description="UVSim - Run a BasicML program")
group = parser.add_mutually_exclusive_group()

group.add_argument("file", type=str, action="store", nargs="?", metavar = "file_path", default = None, help="file path to the BasicML input file")
group.add_argument("-m", "--manual", action="store_true", help="manually enter opcodes instead of reading from a file")
parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose mode for debugging")
parser.add_argument("--version", action="version", version="%(prog)s 1.0")

args = parser.parse_args()

def main():
    io.write("\nWelcome to UVSim - Universal Virtual Simulator")

    if args.verbose:
        cpu.log = True
    
    if args.manual and not args.file:
        io.write("---Manual Instruction Input Mode---")
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
    elif not args.file and not args.manual:
        file_path = io.read_string("Enter the file path to the BasicML input file:\n")
        try:
            io.read_from_file(file_path)
        except FileNotFoundError as e:
            io.write(e, True)
            return
        boot.load_program(file_path)
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