"""CPU for UVSim."""

from .memory import Memory
from termcolor import colored
import difflib
import tkinter as tk
from tkinter import messagebox


class Halt(Exception):
    """Exception used to halt the CPU.

    Has no data - Simply inherits from Exception.
    """

    pass


class CPU:
    """CPU Class - Used for Implmenting the UVSim Project."""

    # Constants
    MAX = 999999
    MIN = -999999
    ACCUMULATOR_DEFAULT = 000000
    REGISTER_DEFAULT = (
        43000  # Halt command is used as Default
    )
    POINTER_DEFAULT = 000000
    # Used for testing purposes - Need to force the CPU to halt in case things go wrong
    MAX_INSTRUCTION_LIMIT = 1000

    def __init__(
        self,
        memory: Memory,
    ):
        """Initialize CPU module, using the boot_up function and default values to clear."""
        self.boot_up()
        self.log = False
        self.halted = True

        self.previous_memory_state = " "
        self.current_memory_state = " "

        self.memory = memory
        self.current_memory_state = str(self.memory)

    def boot_up(self):
        """Clears all values to original defaults, allowing the CPU to be restarted."""
        self.accumulator = CPU.ACCUMULATOR_DEFAULT
        self.register = CPU.REGISTER_DEFAULT
        self.pointer = CPU.POINTER_DEFAULT
        self.halted = False
   
    def _get_memory(self):
        return self.memory

    def print_memory(self):
        """Prints the current state of the CPU/Memory with differences highlighted from the previous state
        Green background: Added text.
        """
        prev_text = self.previous_memory_state
        curr_text = self.current_memory_state        

        if curr_text is None:
            return

        if prev_text is None:
            return curr_text

        matcher = difflib.SequenceMatcher(None, prev_text, curr_text)

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                # Print unchanged text normally
                return curr_text
            elif tag in ["replace", "insert"]:
                # Print new/changed text in green
                return colored(curr_text[j1:j2], "green")

    def run(self, gui=None, cont=False):
        """Creates loop that allows the CPU to run continuously
        Will self-increment to next instruction in memory and read until halted.

        Reads from file_location and saves all the instructions in the memory module
        Memory is then executed

        Parameters:
            file_location - file location to read instructions into memory
        """
        if not cont:
            self.boot_up()
            max_instructions = CPU.MAX_INSTRUCTION_LIMIT
        else:
            max_instructions = CPU.MAX_INSTRUCTION_LIMIT - self.pointer

        while max_instructions > 0:
            self.previous_memory_state = self.current_memory_state
            self.current_memory_state = str(self.memory)
            if not gui is None:
                gui.update_memory_text(self.print_memory())

            try:
                # DO NOT CHANGE UNLESS YOU KNOW EXPLICITLY WHAT IT WILL DO
                # I had to spend almost two hours fixing a bug because someone changes the order of these two line..
                # Pointer MUST be updated first, because otherwise it will jump and THEN skip to the next instruction......
                
                self.register = Memory.word_to_int(self.memory.read(self.pointer))
                self.pointer += 1 
                self.operation(self.register, gui)

            except Halt:
                self.halted = True
                return

            except ValueError as e:
                return f"Error: {e}"

            except KeyboardInterrupt:
                return "Keyboard Interrupt"

            finally:
                max_instructions -= 1

        if max_instructions == 0:
            return "MAX INSTRUCTIONS LIMIT REACHED : Halting"
    
    @staticmethod
    def decypher_instruction(word):
        # Why 10,000? Because if a 6 digit instruciton starts with an operator of 010, it would be 010 000 meaning >= 10,000
        if word >= 10000:
            operator = word // 1000

        elif word < 0:
            # Negative Instructions are invalid
            raise ValueError(f"Negative Operation: {word}")
        
        else:
            #Shouldn't ever occur, all valid operations start at '100 xxx'
            raise ValueError(
                f"Invalid Opeartion: {word} | No opeartions exist under 10000"
            )
        operand = word % 1000

        return (operator, operand)

    def operation(self, word, gui=None, matchAndReturnInstInfo=False):
        """Function to run a specific instruction (word) or return it's name.

        Parameters:
            word - Is validated
            gui - GUI object to interact with the user
            matchAndReturnName - If True, then the name of the instruction is returned only

        Return Values:
            - If matchAndReturnName is True, then the name of the instruction is returned
            - If matchAndReturnName is False, then the instruction is ran and nothing is returned

        Raises:
            ValueError:
                - If Operation is negative
                - If Operation is < 100
                - If Operation is not a valid instruction
            Halt:
                - Instructs the machine to halt if certain conditions are met
        """
        try:
            operator, operand = CPU.decypher_instruction(word)

            match operator:
                # I/O Operations
                case 10:
                    if matchAndReturnInstInfo:
                        return f"{self.memory.int_to_word(word)}: READ (10)\nRead a word from the keyboard into memory location {operand}."
                    self.op_READ(operand, gui)
                case 11:
                    if matchAndReturnInstInfo:
                        return f"{self.memory.int_to_word(word)}: WRITE (11)\nWrite the word from memory location {operand} to screen."
                    self.op_WRITE(operand, gui)

                # Load/Store Operations
                case 20:
                    if matchAndReturnInstInfo:
                        return f"{self.memory.int_to_word(word)}: LOAD (20)\nLoad the word from memory location {operand} into the accumulator."
                    self.op_LOAD(operand)
                case 21:
                    if matchAndReturnInstInfo:
                        return f"{self.memory.int_to_word(word)}: STORE (21)\nStore the word from the accumulator into memory location {operand}."
                    self.op_STORE(operand)

                # Arithmetic Operation
                case 30:
                    if matchAndReturnInstInfo:
                        return f"{self.memory.int_to_word(word)}: ADD (30)\nAdd the word from memory location {operand} to the word in the accumulator (leave the result in the accumulator)"
                    self.op_ADD(operand)
                case 31:
                    if matchAndReturnInstInfo:
                        return f"{self.memory.int_to_word(word)}: SUBTRACT (31)\nSubtract the word from memory location {operand} to the word in the accumulator (leave the result in the accumulator)."
                    self.op_SUBTRACT(operand)
                case 32:
                    if matchAndReturnInstInfo:
                        return f"{self.memory.int_to_word(word)}: DIVIDE (32)\nDivide the word in the accumulator by the word from memory location {operand} (leave the result in the accumulator)."
                    self.op_DIVIDE(operand)
                case 33:
                    if matchAndReturnInstInfo:
                        return f"{self.memory.int_to_word(word)}: MULTIPLY (33)\nMultiply the word from memory location {operand} to the word in the accumulator (leave the result in the accumulator)."
                    self.op_MULTIPLY(operand)

                # Control Operations
                case 40:
                    if matchAndReturnInstInfo:
                        return f"{self.memory.int_to_word(word)}: BRANCH (40)\nBranch to memory location {operand}."
                    self.op_BRANCH(operand)
                case 41:
                    if matchAndReturnInstInfo:
                        return f"{self.memory.int_to_word(word)}: BRANCHNEG (41)\nBranch to memory location {operand} if the accumulator is negative."
                    self.op_BRANCHNEG(operand)
                case 42:
                    if matchAndReturnInstInfo:
                        return f"{self.memory.int_to_word(word)}: BRANCHZERO (42)\nBranch to memory location {operand} if the accumulator is zero."
                    self.op_BRANCHZERO(operand)
                case 43:
                    if matchAndReturnInstInfo:
                        return f"{self.memory.int_to_word(word)}: HALT (43)\nPause the program."
                    # Raises HALT
                    self.op_HALT()

                # Test Operators
                case 99:
                    pass

                # Default Error Case
                case _:
                    raise ValueError(f"Invalid Operation: {operator}")

        except Halt:
            raise Halt

    def read_from_memory(self, address):
        """Transition method to allow for str words to be read into the register
        and then saved as an integer in the register.

        Parameters:
            - address : 2-digit address to read from in memory
        """
        self.register = Memory.word_to_int(self.memory.read(address))

    def load_to_memory(self, address, value):
        """Transition method to allow for integer data in the regsiter
        to be read into the address in the memory module.

        Parameters:
            - address : 2-digit address to read from in memory
            - value : data to be saved in memory - Usually the register
        """
        self.memory.write(address, value)

    def op_READ(self, operand, gui):
        """Mini Method used to read a 6-digit signed instruction from 
        the io_text entry object in the GUI and save it to a specific 
        memory location (operand).

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        def read_input(event):
            check = True
            while (check):
                operand = gui.io_text.get().strip()

                try:
                    gui.input.set(self.memory.word_to_int(operand))
                    check = False
                    break
                except ValueError as e:
                    pass
                
                if check:
                    try:
                        operand = self.memory.int_to_word(int(operand))
                        gui.input.set(self.memory.word_to_int(operand))
                        break
                        
                    except ValueError as e:
                        messagebox.showerror("Error", str(e))
                        gui.root.wait_variable(gui.input)
                        continue
        
        gui.io_text.config(state=tk.NORMAL)
        gui.io_text.delete("0", "end")
        gui.io_text.bind("<Return>", read_input)
        gui.io_label.configure(text="Read a 6-digit signed instruction: (Press enter to submit)")
        gui.input = tk.StringVar()
        gui.root.wait_variable(gui.input)
        gui.io_text.delete("0", "end")
        gui.io_label.configure(text="I/O")
        gui.io_text.unbind("<Return>")
        gui.io_text.config(state=tk.DISABLED)

        self.register = int(gui.input.get().strip())
        self.load_to_memory(operand, self.register)

    def op_WRITE(self, operand, gui):
        """Mini Method used to write data from memory at
        a specific memory location (operand) to the io_text entry object in the GUI.

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        self.read_from_memory(operand)

        if gui is not None:
            gui.io_text.config(state=tk.NORMAL)
            gui.io_label.configure(text="Write Output:")
            gui.io_text.delete(0, tk.END)
            gui.io_text.insert(tk.END, self.memory.int_to_word(self.register))

    def op_LOAD(self, operand):
        """Mini Method used to load a word from memory at the operand location
        to the accumulator.

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        self.read_from_memory(operand)
        self.accumulator = self.register

    def op_STORE(self, operand):
        """Mini Method used to store data from the accumulator to a specific
        location in memory (operand).

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        self.load_to_memory(operand, int(self.accumulator))

    def op_ADD(self, operand):
        """Mini Method used to ADD a word from the data at
        a specific memory location (operand) to the accumulator.

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        self.read_from_memory(operand)
        self.accumulator += self.register

    def op_SUBTRACT(self, operand):
        """Mini Method used to SUBTRACT a word from the data at
        a specific memory location (operand) to the accumulator.

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        self.read_from_memory(operand)
        self.accumulator -= self.register

    def op_MULTIPLY(self, operand):
        """Mini Method used to MULTIPLY a word from the data at
        a specific memory location (operand) to the accumulator.

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        self.read_from_memory(operand)
        self.accumulator *= self.register

    def op_DIVIDE(self, operand):
        """Mini Method used to DIVIDE a word from the data at
        a specific memory location (operand) to the accumulator.

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        self.read_from_memory(operand)
        self.accumulator /= self.register

    def op_BRANCH(self, operand):
        """Mini Method used to branch to the location in memory of the operand.

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        self.pointer = operand

    def op_BRANCHNEG(self, operand):
        """Mini Method used to branch to the location in memory of the operand
        IF the accumulator is ZERO ONLY.

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        if self.accumulator < 0:
            self.op_BRANCH(operand)

    def op_BRANCHZERO(self, operand):
        """Mini Method used to branch to the location in memory of the operand
        IF the accumulator is NEGATIVE ONLY.

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        if self.accumulator == 0:
            self.op_BRANCH(operand)

    def op_HALT(self):
        """Mini Method used to halt the CPU.

        Parameters:
            operand [UNUSED] - Memory Location (2-digits)

        Raises:
            - Halt

        Return - None
        """
        raise Halt


def main():
    from boot import Bootstrapper
    boot = Bootstrapper()

    boot.load_from_file("tests/cpu_test_6digit.txt")
    boot.run(gui=None)

    # with open("tests/cpu_test_final.txt") as file:
    #     final_data = file.readlines()

    #     boot.cpu.read_from_memory(85)
    #     assert 1875 == boot.cpu.register

    #     for i, word in enumerate(final_data):
    #         boot.cpu.read_from_memory(i)
    #         assert Memory.word_to_int(word.strip()) == boot.cpu.register

if __name__ == "__main__":
    main()