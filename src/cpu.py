try:
    from io_handler import IOHandler
except ImportError:
    from .io_handler import IOHandler

try:
    from memory import Memory
except ImportError:
    from .memory import Memory

from termcolor import colored
import difflib

IO = IOHandler()
MEMORY = Memory()

class Halt(Exception):
    """
    Exception used to halt the CPU
    Has no data - Simply inherits from Exception
    """
    pass  

class CPU():
    """
    CPU Class - Used for Implmenting the UVSim Project
    """
    # Constants 
    MAX =  9999
    MIN = -9999    
    ACCUMULATOR_DEFAULT = 0000      
    REGISTER_DEFAULT    = 4300 # Halt command is used as Default | Should be changed eventually
    POINTER_DEFAULT     = 0000
    MAX_INSTRUCTION_LIMIT = 10 # Used for testing purposes - Need to force the CPU to halt in case things go wrong

    def __init__(self):
        """
        Initialize CPU module, using the boot_up function and default values to clear
        """
        self.boot_up()
        self.log = False
        self.halted = True

        self.previous_memory_state = " "
        self.current_memory_state = " "
    
    def boot_up(self):
        """
        Clears all values to their original defaults, thus allowing the CPU to be reset and restarted
        """
        self.accumulator = CPU.ACCUMULATOR_DEFAULT
        self.register = CPU.REGISTER_DEFAULT
        self.pointer = CPU.POINTER_DEFAULT
        self.halted = False

    @staticmethod
    def read_file(file_location):
        """
        Static method that takes a relative file location and
        returns a list of instructions to be passed to the memory module
        """
        data = []
        with open(file_location, 'r') as file:
            for line in file:
                word = line.split()
                data.append(word[0].strip())
        return data
    
    def _get_memory(self):
        return MEMORY
    
    def _get_IO(self):
        return IO
    
    def print_memory_states_DEV_ONLY(self):
        """
        Prints the current state of the CPU/Memory with differences highlighted from the previous state
        Green background: Added text
        """
        prev_text = self.previous_memory_state
        curr_text = self.current_memory_state

        if curr_text is None:
            return
        
        if prev_text is None:
            print(curr_text)
            return          
        
        matcher = difflib.SequenceMatcher(None, prev_text, curr_text)        
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                # Print unchanged text normally
                print(curr_text[j1:j2], end='')
            elif tag in ['replace', 'insert']:
                # Print new/changed text in green
                print(colored(curr_text[j1:j2], 'green'), end='')     


    def run(self, file_location):
        """
        Creates loop that allows the CPU to run continuously
        Will self-increment to next instruction in memory and read until halted

        Reads from file_location and saves all the instructions in the memory module
        Memory is then executed

        Parameters:
            file_location - file location to read instructions into memory
        """
        self.boot_up()
        data = CPU.read_file(file_location)

        try:
            MEMORY.load_program(data)
        except ValueError as e:
            print(e)
            print("Halting Loading : Invalid word is given")
                   

        max_instructions = CPU.MAX_INSTRUCTION_LIMIT
        while (max_instructions > 0):
            self.previous_memory_state = self.current_memory_state
            self.current_memory_state = str(MEMORY) + '\n'  + str(self) + '\n'       
            self.print_memory_states_DEV_ONLY()
                    
            try: 
                self.register = MEMORY.word_to_int(MEMORY.read(self.pointer))
                self.operation(self.register)
                self.pointer += 1

            except Halt:
                self.halted = True
                break     

            except ValueError as e:
                print(e)

            except KeyboardInterrupt:
                print("Keyboard Interrupted")
                break

            finally:
                max_instructions -= 1

        if max_instructions == 0 :
            print ('MAX INSTRUCTIONS LIMIT REACHED : Halting')

    def __str__(self):
        """
        Returns a string of the current state of the CPU
        """
        return f"CPU State\nAccumulator:{self.accumulator}\nRegister:{self.register}\nPointer:{self.pointer}\n"      

        
    @staticmethod
    def _validate(word):    
        """
        Static Method used to validate a word
        Word must be a signed 4-digit integer

        Parameters:
            word (int)

        Return Values:
            True - If word is valid

        Raises:
            ValueError: 
                - If word is invalid, either not an intger or out of range
        """    
        if not isinstance(word, int):
            raise ValueError(f'VALIDATION FAIL: Not an Integer: {word}')
        
        if not CPU.MIN <= word <= CPU.MAX:
            raise ValueError(f'VALIDATION FAIL: Out of Range: {word}')
        
        return True

    # def validate(func):
    #     def wrapper(*args, **kwargs):
    #         try:
    #             if CPU._validate(args[1]):
    #                 return func(*args, **kwargs)
    #         except ValueError as e:
    #             print(e)
    #     return wrapper

    @staticmethod
    def decypher_instruction(word):
        """
        Decypher instruction is a static method used to split a 4 digit instruction
        into an operator an operand
        
        ASSUMES _validate(word) has been ran before hand. This is because some words are not valid 
        instructions but are valid 4-digit 'words'

        Parameters:
            - word : validated word is passed to split 4 digits into the first two and last two digits

        Raises:
            ValueError : If a word is not a valid instruction (negative or below 1000)
        """

        if word >= 1000:
            operator = word // 100

        elif word < 0:
            # Not sure what to do with negative instructions yet
            raise ValueError(f"Negative Operation: {word}")

        else: 
            #Shouldn't ever actually occur, because all valid operations start at '10xx'
            raise ValueError(f"Invalid Operation: {word} | No operations exist under 1000")

        operand = word % 100

        return (operator, operand)

    
    def operation(self, word):
        """
        Function to run a specific instruction (word)
        Instruction function is then ran

        Parameters:
            word - Is validated

        Return Values:
            None

        Raises:
            ValueError: 
                - If Operation is negative
                - If Operation is < 100 
                - If Operation is not a valid instruction
            Halt:
                - Instructs the machine to halt if certain conditions are met
        """
        try:
            CPU._validate(word)       
            operator, operand = CPU.decypher_instruction(word)

            match operator:
                # I/O Operations
                case 10: 
                    self.op_READ(operand)
                case 11:
                    self.op_WRITE(operand)
                                
                # Load/Store Operations
                case 20:
                    self.op_LOAD(operand)
                case 21:
                    self.op_STORE(operand)

                #Arithmetic Operation
                case 30:
                    self.op_ADD(operand)
                case 31:
                    self.op_SUBTRACT(operand)
                case 32:
                    self.op_DIVIDE(operand)
                case 33:
                    self.op_MULTIPLY(operand)

                # Control Operations
                case 40:
                    self.op_BRANCH(operand)
                case 41:
                    self.op_BRANCHNEG(operand)
                case 42:
                    self.op_BRANCHZERO(operand)
                case 43:
                    # Raises HALT
                    self.op_HALT(operand)

                # Test Operators
                case 99:
                    pass

                #Default Error Case
                case _:
                    raise ValueError(f"Invalid Operation: {word}")

        except Halt:
            raise Halt 

    def read_from_memory(self, address):
        """
        Transition method to allow for str words to be read into the register
        and then saved as an integer in the register

        Parameters:
            - address : 2-digit address to read from in memory
        """
        self.register = MEMORY.word_to_int(MEMORY.read(address))     

    def load_to_memory(self, address, value):        
        """
        Transition method to allow for integer data in the regsiter
        to be read into the address in the memory module

        Parameters:
            - address : 2-digit address to read from in memory
            - value : data to be saved in memory - Usually the register
        """
        MEMORY.write(address, MEMORY.int_to_word(value))            

    def op_READ(self, operand):
        """
        Mini Method used to read a 4-digit signed instruction from the CMD
        to a specific memory location (operand)

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """        
        self.register = int(IO.read_operation('4-digit signed instruction | READ: '))
        self.load_to_memory(operand, self.register)
    
    def op_WRITE(self, operand):
        """
        Mini Method used to write data from memory at
        a specific memory location (operand) to the CMD or STDOUT

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """  
        self.read_from_memory(operand)
        IO.write(self.register, log=self.log)

    def op_LOAD(self, operand):  
        """
        Mini Method used to load a word from memory at the operand location
        to the accumulator

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """        
        self.read_from_memory(operand)
        self.accumulator = self.register   

    def op_STORE(self, operand):
        """
        Mini Method used to store data from the accumulator to a specific
        location in memory (operand)

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """  
        self.load_to_memory(operand, self.accumulator)

    def op_ADD(self, operand):
        """
        Mini Method used to ADD a word from the data at 
        a specific memory location (operand) to the accumulator

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """  
        self.read_from_memory(operand)
        self.accumulator += self.register

    def op_SUBTRACT(self, operand):
        """
        Mini Method used to SUBTRACT a word from the data at 
        a specific memory location (operand) to the accumulator

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """  
        self.read_from_memory(operand)
        self.accumulator -= self.register

    def op_MULTIPLY(self, operand):
        """
        Mini Method used to MULTIPLY a word from the data at 
        a specific memory location (operand) to the accumulator

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        self.read_from_memory(operand)
        self.accumulator *= self.register

    def op_DIVIDE(self, operand):
        """
        Mini Method used to DIVIDE a word from the data at 
        a specific memory location (operand) to the accumulator

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """ 
        self.read_from_memory(operand)
        self.accumulator /= self.register

    def op_BRANCH(self, operand):
        """
        Mini Method used to branch to the location in memory of the operand

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        self.read_from_memory(operand)
        self.pointer = self.register

    def op_BRANCHNEG(self, operand):
        """
        Mini Method used to branch to the location in memory of the operand
        IF the accumulator is ZERO ONLY

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """
        if self.accumulator < 0:
            self.op_BRANCH(operand)

    def op_BRANCHZERO(self, operand):
        """
        Mini Method used to branch to the location in memory of the operand
        IF the accumulator is NEGATIVE ONLY

        Parameters:
            operand - Memory Location (2-digits)

        Return - None
        """  
        if self.accumulator == 0:
            self.op_BRANCH(operand)

    def op_HALT(self, operand): 
        """
        Mini Method used to halt the CPU

        Parameters:
            operand [UNUSED] - Memory Location (2-digits)            

        Raises:
            - Halt

        Return - None
        """         
        raise Halt       

def main():
    cpu = CPU()
    cpu.run('Test1.txt')    
         
if __name__ == "__main__":
    main()
    
        

        







