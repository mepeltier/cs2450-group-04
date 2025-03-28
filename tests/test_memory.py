import pytest
from src.memory import Memory


def test_memory_initialization():
    memory = Memory()
    assert len(memory.memory) == 250
    assert memory.memory[0] == "+000000"
    assert memory.memory[99] == "+000000"


def test_memory_read_write():
    memory = Memory()
    memory.write(0, "+001234")
    assert memory.read(0) == "+001234"


def test_invalid_address():
    memory = Memory()
    with pytest.raises(IndexError):
        memory.read(250)
    with pytest.raises(IndexError):
        memory.write(250, "+001234")


def test_invalid_word_format():
    memory = Memory()
    invalid_words = ["001234", "++001234", "+00123", "+0012345", "+00abcd"]
    for word in invalid_words:
        with pytest.raises(ValueError):
            memory.write(0, word)


def test_clear_memory():
    memory = Memory()
    memory.write(0, "+001234")
    memory.clear()
    assert memory.read(0) == "+000000"


def test_word_to_int():
    memory = Memory()
    assert memory.word_to_int("+001234") == 1234
    assert memory.word_to_int("-005678") == -5678


def test_int_to_word():
    memory = Memory()
    assert memory.int_to_word(1234) == "+001234"
    assert memory.int_to_word(-5678) == "-005678"
    with pytest.raises(ValueError):
        memory.int_to_word(1000000)


def test_memory_string_representation():
    memory = Memory(size=20)  # Smaller size for easier testing
    memory.write(0, "+001111")
    memory.write(10, "-002222")
    expected = (
        "     00    01    02    03    04    05    06    07    08    09   \n"
        "\xa000 +001111 +000000 +000000 +000000 +000000 +000000 +000000 +000000 +000000 +000000\n"
        "\xa010 -002222 +000000 +000000 +000000 +000000 +000000 +000000 +000000 +000000 +000000"
    )
    assert str(memory) == expected
