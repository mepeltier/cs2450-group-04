from io_handler import IOHandler 

IO = IOHandler()

class Halt(Exception):
            pass

class CPU():
    # Constants 
    MAX = 9999
    MIN = -9999    

    def __init__(self):
        self.register = 0000 # Default for easy testing
        self.accumulator = 0000
        self.memory = None
        self.log = False

    

    def run(self):
        while (True):
            try: 
                self.operation(self.register)
            except Halt:
                break           

        
    @staticmethod
    def _validate(word):        
        if not isinstance(word, int):
            raise ValueError('Not an Integer')
        
        if not CPU.MIN <= word <= CPU.MAX:
            raise ValueError('Out of Range')
        
        return True

    # def validate(func):
    #     def wrapper(*args, **kwargs):
    #         try:
    #             if CPU._validate(args[1]):
    #                 return func(*args, **kwargs)
    #         except ValueError as e:
    #             print(e)
    #     return wrapper

    
    def operation(self, word):
        try:
            CPU._validate(word)              
       
            if word >= 100 and word >= 0:
                operator = word // 100

            elif word < 0:
                # Not sure what to do with negative operators yet
                raise ValueError(f"Negative Operation: {word}")

            else: 
                #Shouldn't ever actually occur, because all valid operations start at '10xx'
                raise ValueError(f"Invalid Operation: {word} | No operations exist under 1000")

            operand = word % 100

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
                case _:
                    raise ValueError(f"Invalid Operation: {word}")
                
        except ValueError as e:
            print(e)

        except Halt:
            raise Halt

            

    def op_READ(self, operand):
        x = int(IO.read_operation(''))
        # TODO WRITE X TO MEMORY     

    
    def op_WRITE(self, operand):
        # TODO Get X FROM MEMORY
        IO.write(operand, log=self.log)

    def op_LOAD(self, operand):
        # TODO Get X FROM MEMORY
        x = 1000 # Default Value until Memory Module is ready
        if CPU._validate(x):
            self.accumulator = x   

    def op_STORE(self, operand):
        # TODO Store X into Memory
        # memory.store(self.accumulator)
        pass

    def op_ADD(self, operand):
        # TODO Get X from Memory
        x = 1 # Default Value
        # x = memory.load(operand)

        self.accumulator += x

    def op_SUBTRACT(self, operand):
        # TODO Get X from Memory
        x = 1 # Default Value
        # x = memory.load(operand)

        self.accumulator -= x

    def op_MULTIPLY(self, operand):
        # TODO Get X from Memory
        x = 1 # Default Value
        # x = memory.load(operand)

        self.accumulator *= x

    def op_DIVIDE(self, operand):
        # TODO Get X from Memory
        x = 1 # Default Value
        # x = memory.load(operand)

        self.accumulator /= x

    def op_BRANCH(self, operand):
        # TODO Branch using memory module..?
        pass

    def op_BRANCHNEG(self, operand):
        if self.accumulator < 0:
            self.op_BRANCH(operand)

    def op_BRANCHZERO(self, operand):
        if self.accumulator == 0:
            self.op_BRANCH(operand)

    def op_HALT(self, operand):        
        raise Halt       

def main():
    cpu = CPU()
    cpu.run()
    

if __name__ == "__main__":
    main()
        

        







