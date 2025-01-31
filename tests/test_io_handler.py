import pytest
from cs2450_group_04.io_handler import IOHandler
from unittest.mock import patch, mock_open


def test_read_operation_valid():
    io_handler = IOHandler()
    with patch("builtins.input", side_effect=["1234"]):
        assert io_handler.read_operation("Enter a number: ") == 1234


def test_read_operation_invalid_then_valid():
    io_handler = IOHandler()
    with patch("builtins.input", side_effect=["abcd", "10000", "-10000", "4321"]):
        assert io_handler.read_operation("Enter a number: ") == 4321


def test_write_print():
    io_handler = IOHandler()
    with patch("builtins.print") as mock_print:
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
    with patch("builtins.input", side_effect=["1"]):
        assert io_handler.read_choice("Select an option:", choices) == "1"


def test_read_choice_invalid_then_valid():
    io_handler = IOHandler()
    choices = {"1": "Option 1", "2": "Option 2"}
    with patch("builtins.input", side_effect=["3", "2"]):
        assert io_handler.read_choice("Select an option:", choices) == "2"


def test_read_yes_no_valid():
    io_handler = IOHandler()
    with patch("builtins.input", side_effect=["yes"]):
        assert io_handler.read_yes_no("Do you want to continue?") is True
    with patch("builtins.input", side_effect=["no"]):
        assert io_handler.read_yes_no("Do you want to continue?") is False


def test_read_yes_no_invalid_then_valid():
    io_handler = IOHandler()
    with patch("builtins.input", side_effect=["maybe", "y"]):
        assert io_handler.read_yes_no("Do you want to continue?") is True
    with patch("builtins.input", side_effect=["what", "n"]):
        assert io_handler.read_yes_no("Do you want to continue?") is False


def test_read_string_valid():
    io_handler = IOHandler()
    with patch("builtins.input", side_effect=["Valid String"]):
        assert io_handler.read_string("Enter a string:") == "Valid String"


def test_read_string_invalid_then_valid():
    io_handler = IOHandler()
    with patch("builtins.input", side_effect=["", "A valid response"]):
        assert io_handler.read_string("Enter a string:") == "A valid response"


def test_read_from_file():
    io_handler = IOHandler()
    mock_data = "Line 1\nLine 2\nLine 3\n"
    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
        result = io_handler.read_from_file("test_file.txt")
        assert result == ["Line 1", "Line 2", "Line 3"]
        mock_file.assert_called_once_with("test_file.txt", "r")


def test_read_from_file_not_found():
    io_handler = IOHandler()
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = io_handler.read_from_file("missing_file.txt")
        assert result == []
