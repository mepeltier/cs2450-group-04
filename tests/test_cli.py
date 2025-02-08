from unittest.mock import patch
import importlib
import pytest
import sys
import io


def test_file_mode():
    '''
    Tests that the program loads a file and runs it when a file path is provided on the command line.
    '''
    testargs = ["UVSim", "test.txt"]
    with patch.object(sys, 'argv', testargs):
        import src.main as main
        importlib.reload(main)
        with patch.object(main.boot, 'load_program') as mock_load, \
             patch.object(main.boot, 'run') as mock_run:
            main.main()
            mock_load.assert_called_once_with("test.txt")
            mock_run.assert_called_once()

def test_interactive_mode():
    '''
    Tests that the program prompts the user for a file path when no file is provided.
    '''
    testargs = ["UVSim"]
    with patch.object(sys, 'argv', testargs):
        import src.main as main
        importlib.reload(main)
        with patch.object(main.boot.io, 'read_string', return_value="test.txt") as mock_read_str, \
             patch.object(main.boot.io, 'read_from_file') as mock_read_file, \
             patch.object(main.boot, 'load_program') as mock_load, \
             patch.object(main.boot, 'run') as mock_run:
            main.main()
            mock_read_str.assert_called_once_with("Enter the file path to the BasicML input file (type 'manual' to start typing instructions):\n")
            mock_read_file.assert_called_once_with("test.txt")
            mock_load.assert_called_once_with("test.txt")
            mock_run.assert_called_once()

def test_manual_mode():
    '''
    Tests that the program enters manual mode when the -m flag is provided by simulating two valid instructions are entered and then END.
    '''
    testargs = ["UVSim", "-m"]
    with patch.object(sys, 'argv', testargs):
        import src.main as main
        importlib.reload(main)
        side_effects = ["+1001", "+1002", "END"]
        with patch.object(main.boot.io, 'read_string', side_effect=side_effects) as mock_read_str, \
             patch.object(main.boot.memory, 'validate_word') as mock_validate_word, \
             patch.object(main.boot.memory, 'write') as mock_mem_write, \
             patch.object(main.boot, 'run') as mock_run:
            main.main()
            assert mock_read_str.call_count == 3
            assert mock_validate_word.call_count == 2
            calls = mock_mem_write.call_args_list
            assert len(calls) == 2
            assert calls[0][0] == (0, "+1001")
            assert calls[1][0] == (1, "+1002")
            mock_run.assert_called_once()

def test_verbose_mode():
    '''
    Tests that the program enters verbose mode when the -v flag is provided.
    '''
    testargs = ["UVSim", "-v", "test.txt"]
    with patch.object(sys, 'argv', testargs):
        import src.main as main
        importlib.reload(main)
        with patch.object(main.boot, 'load_program') as mock_load, \
             patch.object(main.boot, 'run') as mock_run:
            main.main()
            mock_load.assert_called_once_with("test.txt")
            mock_run.assert_called_once()
            assert main.boot.cpu.log is True

def test_version():
    '''
    Tests the --version flag to ensure it prints the correct version number.
    '''
    testargs = ["UVSim", "--version"]
    with patch('sys.stdout', new_callable=io.StringIO) as fake_stdout, \
         patch.object(sys, 'argv', testargs):
        import src.main as main
        with pytest.raises(SystemExit):
            importlib.reload(main)
        output = fake_stdout.getvalue()
        assert "UVSim 1.0" in output

def test_help_message():
    '''
    Tests that the help message is displayed when the program is ran with the -h flag.
    '''
    testargs = ["UVSim", "-h"]
    with patch('sys.stdout', new_callable=io.StringIO) as fake_stdout, \
         patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit):
            import src.main as main
            importlib.reload(main)
        output = fake_stdout.getvalue()
        assert "usage:" in output
        assert "UVSim - Run a BasicML program" in output
