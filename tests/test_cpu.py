import pytest
import unittest
from src.cpu import CPU

class TestCPU(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()

    def tearDown(self):
        pass        

    def test_CPU_init(self):
        assert isinstance(self.cpu, CPU)

