from io_handler import IOHandler 

IO = IOHandler()

class Halt(Exception):
            pass  

class CPU():
    # Constants 
    MAX =  9999
    MIN = -9999    
    ACCUMULATOR_DEFAULT = 0000      
    REGISTER_DEFAULT    = 0000
    POINTER_DEFAULT     = 0000

    def __init__(self):
        self.boot_up()
        self.log = False
    
    def boot_up(self):
        self.accumulator = CPU.ACCUMULATOR_DEFAULT
        self.register = CPU.REGISTER_DEFAULT
        self.pointer = CPU.POINTER_DEFAULT

    def run(self):
        self.boot_up()

        while (True):
            try: 
                print(self)
                self.operation(self.register)
                self.pointer += 1
            except Halt:
                break     
            except KeyboardInterrupt:
                print("Keyboard Interrupted")
                break

    def __str__(self):
        return f"CPU State\nAccumulator:{self.accumulator}\nRegister:{self.register}\n{self.pointer}\n"      

        
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

                # Test Operators
                case 99:
                    pass

                #Default Error Case
                case _:
                    raise ValueError(f"Invalid Operation: {word}")
                
        except ValueError as e:
            print(e)

        except Halt:
            raise Halt      
            

    def op_READ(self, operand):        
        x = int(IO.read_operation('4-digit signed instruction | READ: '))
        # TODO WRITE X TO MEMORY    
        return x        
    
    def op_WRITE(self, operand):
        # TODO Get X FROM MEMORY
        IO.write(operand, log=self.log)

    def op_LOAD(self, operand):        
        # TODO Get X FROM MEMORY
        # self.register = memory.load(operand)
        if CPU._validate(self.register):
            self.accumulator = self.register       

    def op_STORE(self, operand):
        # TODO Store X into Memory
        # memory.store(self.accumulator)
        pass

    def op_ADD(self, operand):
        # TODO Get x from Memory
        # self.register = memory.load(operand)
        self.accumulator += self.register

    def op_SUBTRACT(self, operand):
        # TODO Get X from Memory
        x = 1 # Default Value
        # self.register = memory.load(operand)
        self.accumulator -= self.register

    def op_MULTIPLY(self, operand):
        # TODO Get X from Memory
        x = 1 # Default Value
        # x = memory.load(operand)
        self.accumulator *= self.register

    def op_DIVIDE(self, operand):
        # TODO Get X from Memory
        # self.register = memory.load(operand)
        self.accumulator /= self.register

    def op_BRANCH(self, operand):
        # TODO Branch using memory module..?
        self.register = operand
        # memory.branch(self.register)

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
        

        







