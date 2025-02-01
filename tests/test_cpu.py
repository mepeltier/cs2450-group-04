import pytest # type: ignore
import unittest

if __name__ != "__main__":
    from src.cpu import CPU, MEMORY, IO
    from src.cpu import Halt

class TestCPU(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()            
        MEMORY.load_program(CPU.read_file('tests/cpu_test.txt', fix_index=True))

    def tearDown(self):
        pass        

    def test_CPU_init(self):
        assert isinstance(self.cpu, CPU)

    def test_validate(self):
        invalid_words = [-10_000, 10_000, -42.5, 1/2, 'Test', float(2)]
        
        for w in invalid_words:
            with pytest.raises(ValueError):
                CPU._validate(w)

    def test_bad_operations(self):
        bad_operations = [0, -10, -9999, 100, 999, 1200, 2200, 3400, 4400]

        for o in bad_operations:
            with pytest.raises(ValueError):
                self.cpu.operation(o)

    def test_decypher_instruction(self):
        """
        Tests that the decypher word function is correclty splitting a 4-digit
        instruction into an operator and operand
        """
        instructions = [
            1000,
            2000,
            2300,
            4599,
            5301,
            9999
        ]

        correct_operations_and_operands = [
            (10, 00),
            (20, 00),
            (23, 00),
            (45, 99), 
            (53,  1),
            (99, 99)
        ]

        for i, word in enumerate(instructions):
            assert CPU.decypher_instruction(word) == correct_operations_and_operands[i]

    def test_decypher_instruction_errors(self):
        invalid_instructions = [999, 100, 1, 0, -1, -1000, -9999]

        for i in invalid_instructions:
            with pytest.raises(ValueError):
                CPU.decypher_instruction(i)

    def test_read_file(self):
        self.cpu.read_from_memory(10) # Line 10 on .txt file - Memory file has index fixed in tests
        assert self.cpu.register == 8 # Memory address contains the numer '+0008'

    def test_halt(self):
        with pytest.raises(Halt):
            self.cpu.operation(4300)

    def test_READ(self):
        pass
    
    def test_WRITE(self):
        pass

    def test_LOAD(self):
        self.cpu.operation(2010) # Load from [10] 
        assert self.cpu.accumulator == 8

        self.cpu.operation(2011) # Load from [11] 
        assert self.cpu.accumulator == 16

    def test_STORE(self):
        self.cpu.operation(2010) # Load #0008 from [10] into accumulator
        self.cpu.operation(2100) # Store #0008 into [00] in Memory
        assert MEMORY.word_to_int(MEMORY.read(00)) == 8

        self.cpu.operation(2000) # Load #0008 from [00] into register
        assert self.cpu.register == 8

    def test_ADD(self):
        self.cpu.operation(2010) # Load #0008 from [10] into accumulator
        self.cpu.operation(3011) # Add #0016 from [11] into accumulator
        assert self.cpu.accumulator == 8 + 16

    def test_SUBTRACT(self):
        self.cpu.operation(2010) # Load #0008 from [10] into accumulator
        self.cpu.operation(3112) # Subtract #0007 from [12] into accumulator
        assert self.cpu.accumulator == 8 - 7

    def test_MULTIPLY(self):
        self.cpu.operation(2010) # Load #0008 from [10] into accumulator
        self.cpu.operation(3312) # Multiply #0007 from [12] into accumulator
        assert self.cpu.accumulator == 8 * 7

    def test_DIVIDE(self):
        self.cpu.operation(2011) # Load #0016 from [11] into accumulator
        self.cpu.operation(3210) # Divide by #0008 from [10]
        assert self.cpu.accumulator == 16 / 8

    def test_BRANCH(self):
        pass

    def test_BRANCHNEG(self):
        pass

    def test_BRANCHZERO(self):
        pass

    def test_FULL_PROGRAM(self):
        cpu = CPU()
        cpu.run('tests/cpu_test.txt', fix_index=True)
        final_data = cpu.read_file('tests/cpu_test_final.txt')

        cpu.read_from_memory(85)
        assert 1875 == cpu.register
        
        for i, word in enumerate(final_data):
            cpu.read_from_memory(i)
            assert MEMORY.word_to_int(word) == cpu.register





      
        