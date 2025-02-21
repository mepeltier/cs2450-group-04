import pytest
from src.memory import Memory


def test_memory_initialization():
    memory = Memory()
    assert len(memory.memory) == 100
    assert memory.memory[0] == "+0000"
    assert memory.memory[99] == "+0000"


def test_memory_read_write():
    memory = Memory()
    memory.write(0, "+1234")
    assert memory.read(0) == "+1234"


def test_invalid_address():
    memory = Memory()
    with pytest.raises(IndexError):
        memory.read(100)
    with pytest.raises(IndexError):
        memory.write(100, "+1234")


def test_invalid_word_format():
    memory = Memory()
    invalid_words = ["1234", "++1234", "+123", "+12345", "+abcd"]
    for word in invalid_words:
        with pytest.raises(ValueError):
            memory.write(0, word)


def test_clear_memory():
    memory = Memory()
    memory.write(0, "+1234")
    memory.clear()
    assert memory.read(0) == "+0000"


def test_word_to_int():
    memory = Memory()
    assert memory.word_to_int("+1234") == 1234
    assert memory.word_to_int("-5678") == -5678


def test_int_to_word():
    memory = Memory()
    assert memory.int_to_word(1234) == "+1234"
    assert memory.int_to_word(-5678) == "-5678"
    with pytest.raises(ValueError):
        memory.int_to_word(10000)


def test_memory_string_representation():
    memory = Memory(size=20)  # Smaller size for easier testing
    memory.write(0, "+1111")
    memory.write(10, "-2222")
    expected = (
        "            00        01        02        03        04        05        06        07        08        09       \n"
        "00 +1111 +0000 +0000 +0000 +0000 +0000 +0000 +0000 +0000 +0000\n"
        "10 -2222 +0000 +0000 +0000 +0000 +0000 +0000 +0000 +0000 +0000"
    )
    assert str(memory) == expected
