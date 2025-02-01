import pytest # type: ignore
import unittest
from src.cpu import CPU, MEMORY, IO
from src.cpu import Halt

class TestCPU(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()            
        MEMORY.load_program(self.cpu.read_file('tests/cpu_test.txt'))

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
        self.cpu.read_from_memory(10 - 1) # Line 10 on .txt file but memory is zero-indexed
        assert self.cpu.register == 8 # Memory address contains the numer '+0008'

    def test_halt(self):
        with pytest.raises(Halt):
            self.cpu.operation(4300)

    def test_READ(self):
        pass
    
    def test_WRITE(self):
        pass

    def test_LOAD(self):
        pass

    def test_STORE(self):
        pass

    def test_ADD(self):
        pass

    def test_SUBTRACT(self):
        pass

    def test_MULTIPLY(self):
        pass

    def test_DIVIDE(self):
        pass

    def test_BRANCH(self):
        pass

    def test_READ(self):
        pass
    


      
        