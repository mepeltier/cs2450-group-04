import pytest
from src.io_handler import IOHandler
from unittest.mock import patch, mock_open

def test_read_operation_valid():
    io_handler = IOHandler()
    with patch('builtins.input', side_effect=['1234']):
        assert io_handler.read_operation("Enter a number: ") == 1234

def test_read_operation_invalid_then_valid():
    io_handler = IOHandler()
    with patch('builtins.input', side_effect=['abcd', '10000', '-10000', '4321']):
        assert io_handler.read_operation("Enter a number: ") == 4321

def test_write_print():
    io_handler = IOHandler()
    with patch('builtins.print') as mock_print:
        io_handler.write("Hello, World!")
        mock_print.assert_called_once_with("Hello, World!")

def test_write_log():
    io_handler = IOHandler(log_file="test.log")
    with patch("builtins.open", mock_open()) as mock_file:
        io_handler.write("Logging test", log=True)
        mock_file.assert_called_once_with("test.log", "a")
        mock_file().write.assert_called_once_with("Logging test\n")

def test_read_choice_valid():
    io_handler = IOHandler()
    choices = {"1": "Option 1", "2": "Option 2"}
    with patch('builtins.input', side_effect=['1']):
        assert io_handler.read_choice("Select an option:", choices) == "1"

def test_read_choice_invalid_then_valid():
    io_handler = IOHandler()
    choices = {"1": "Option 1", "2": "Option 2"}
    with patch('builtins.input', side_effect=['3', '2']):
        assert io_handler.read_choice("Select an option:", choices) == "2"
