import pytest
import unittest
from src.cpu import CPU
from src.cpu import Halt

class TestCPU(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()

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

    def test_ARITHMATIC(self):
        # ADD

        # SUBTRACT

        # MULTIPLY

        # DIVIDE
        pass

    def test_BRANCH(self):
        pass

    def test_READ(self):
        pass
    


      
        