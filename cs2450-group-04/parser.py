"""Module for parsing BasicML files into memory."""

from instruction_set import InstructionSet


class Parser:
    """Parse a text file into BasicML commands."""

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def parse_command(self):

        with open(file=self.file_name) as f:
            commands = f.readlines()
            for index, command in enumerate(commands):

                # TODO: We're told to assume that the signs of all BasicML commands is `+`
                # Both example files include data at the end of the file, with negative
                # values. We should probably still load those into memory, as we receive
                # them, and raise an error if we hit a negative value as

                if command[0] == "-":
                    command = int(command)

                # TODO: I'm assuming `memory` will be or have a dictionary, that we
                # can do something like memory[index] = command

                else:

                    if len(command) != 4:
                        # TODO: we need to decide what to do here:
                        #   A) we raise an error and break
                        #   B) we raise an error, but try to continue running
                        #   C) we use the first 4 digits / backfill the digits with 0s
                        pass

                    opcode = int(command[:2])
                    address = int(command[2:])

                    if opcode not in InstructionSet:
                        # TODO: Or we can zero out that command and skip it,
                        # depends on what we decide
                        raise ValueError("Opcode `%s` not in instruction set.", opcode)

                    # TODO: I'm assuming `memory` will be or have a dictionary, that we
                    # can do something like memory[index] = command, and then
                    # when we're ready to run the command, we do
                    # instruction = INSTRUCTIONS[opcode](address)
