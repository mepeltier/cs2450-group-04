import pytest  # type: ignore
import unittest

if __name__ != "__main__":
    from src.cpu import CPU, Halt
    from src.memory import Memory
    from src.boot import Bootstrapper



class TestCPU(unittest.TestCase):

    def setUp(self):
        boot = Bootstrapper()
        self.cpu = boot.cpu
        boot.load_from_file("tests/cpu_test_6digit.txt")

    def tearDown(self):
        pass

    def test_CPU_init(self):
        assert isinstance(self.cpu, CPU)

    def test_bad_operations(self):
        bad_operations = [0, -10, -9999, 100, 999, 1200, 2200, 3400, 4400]

        for o in bad_operations:
            with pytest.raises(ValueError):
                self.cpu.operation(o, gui=None)

    def test_decypher_instruction(self):
        """
        Tests that the decypher word function is correclty splitting a 4-digit
        instruction into an operator and operand
        """
        instructions = [10000, 20000, 23000, 45099, 53001, 99099]

        correct_operations_and_operands = [
            (10, 00),
            (20, 00),
            (23, 00),
            (45, 99),
            (53, 1),
            (99, 99),
        ]

        for i, word in enumerate(instructions):
            assert CPU.decypher_instruction(word) == correct_operations_and_operands[i]

    def test_decypher_instruction_errors(self):
        invalid_instructions = [999, 100, 1, 0, -1, -1000, -9999]

        for i in invalid_instructions:
            with pytest.raises(ValueError):
                CPU.decypher_instruction(i)

    def test_read_file(self):
        assert self.cpu.register != 8
        self.cpu.read_from_memory(
            10
        )  
        assert self.cpu.register == 8  # Memory address contains the numer '+0008'

    def test_halt(self):
        with pytest.raises(Halt):
            self.cpu.operation(43000)
    
    def test_LOAD(self):
        assert self.cpu.accumulator != 8
        self.cpu.operation(20010)  # Load from [10]
        assert self.cpu.accumulator == 8

        self.cpu.operation(20011)  # Load from [11]
        assert self.cpu.accumulator == 16

    def test_STORE(self):
        assert self.cpu.register != 8
        self.cpu.operation(20010)  # Load #0008 from [10] into accumulator
        self.cpu.operation(21000)  # Store #0008 into [00] in Memory
        assert Memory.word_to_int(self.cpu.memory.read(00)) == 8

        self.cpu.operation(20000)  # Load #0008 from [00] into register
        assert self.cpu.register == 8

    def test_ADD(self):
        assert self.cpu.accumulator != 8 + 16
        self.cpu.operation(20010)  # Load #0008 from [10] into accumulator
        self.cpu.operation(30011)  # Add #0016 from [11] into accumulator
        assert self.cpu.accumulator == 8 + 16

    def test_SUBTRACT(self):
        assert self.cpu.accumulator != 8 - 7
        self.cpu.operation(20010)  # Load #0008 from [10] into accumulator
        self.cpu.operation(31012)  # Subtract #0007 from [12] into accumulator
        assert self.cpu.accumulator == 8 - 7

    def test_MULTIPLY(self):
        assert self.cpu.accumulator != 8 * 7
        self.cpu.operation(20010)  # Load #0008 from [10] into accumulator
        self.cpu.operation(33012)  # Multiply #0007 from [12] into accumulator
        assert self.cpu.accumulator == 8 * 7

    def test_DIVIDE(self):
        assert self.cpu.accumulator != 16 /8
        self.cpu.operation(20011)  # Load #0016 from [11] into accumulator
        self.cpu.operation(32010)  # Divide by #0008 from [10]
        assert self.cpu.accumulator == 16 / 8 

    def test_BRANCH(self):
        assert self.cpu.pointer != 59
        self.cpu.operation(40059)  # Tests that the CPU has it's pointer updated to 59, should NOT increment after jumping
        assert self.cpu.pointer == 59

    def test_BRANCHZERO(self):
        assert self.cpu.pointer != 59
        self.cpu.operation(20010)  # Load #0008 from [10] into accumulator
        self.cpu.operation(31010)  # Subtract #0008 from accumulator (0)
        self.cpu.operation(42059)  # Branches to 59 if accumulator is ZERO
        assert self.cpu.pointer == 59

    def test_BRANCHNEG(self):
        assert self.cpu.pointer !=59
        self.cpu.operation(20010)  # Load #0008 from [10] into accumulator
        self.cpu.operation(31011)  # Subtract #0016 from accumulator (-8)
        self.cpu.operation(41059)  # Branches to 59 if accumulator is NEGATIVE
        assert self.cpu.pointer == 59

    # def test_FULL_PROGRAM(self):
    #     boot = Bootstrapper()

    #     boot.load_from_file("tests/cpu_test.txt")
    #     boot.run(gui=None)
    #     with open("tests/cpu_test_final.txt") as file:
    #         final_data = file.readlines()

    #         boot.cpu.read_from_memory(85)
    #         assert 1875 == boot.cpu.register

    #         for i, word in enumerate(final_data):
    #             boot.cpu.read_from_memory(i)
    #             assert Memory.word_to_int(word.strip()) == boot.cpu.register

