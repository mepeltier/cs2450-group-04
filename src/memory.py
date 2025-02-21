"""Memory module."""


class Memory:
    """Memory functionality."""

    def __init__(self, size=100):
        """Initialize memory with specified size (default 100 words).

        Each word is initialized to +0000.
        """
        self.size = size
        self.memory = ["+0000"] * size

    def validate_address(self, address):
        """Validate if the memory address is within bounds.

        Parameters:
        address (int): Memory address to validate

        Raises:
        IndexError: If address is out of bounds
        """
        if not (0 <= address < self.size):
            raise IndexError(
                f"Memory address {address} out of bounds. Valid range: 0-{self.size-1}"
            )

    @staticmethod
    def validate_word(word):
        """Validate if a word is a valid signed four-digit decimal number.

        Parameters:
        word (str): Word to validate

        Raises:
        ValueError: If word format is invalid
        """
        if not isinstance(word, str):
            raise ValueError("Word must be a string")

        if len(word) != 5:  # +/- and 4 digits
            raise ValueError("Word must be 5 characters long (sign + 4 digits)")

        if word[0] not in ["+", "-"]:
            raise ValueError("Word must start with + or -")

        if not word[1:].isdigit():
            raise ValueError("Last 4 characters must be digits")

    def read(self, address):
        """Read a word from the specified memory address.

        Parameters:
        address (int): Memory address to read from

        Returns:
        str: Word at specified address
        """
        self.validate_address(address)
        return self.memory[address]

    def write(self, address: int, word: int | str):
        """Write a word to the specified memory address.

        Parameters:
        address (int): Memory address to write to
        word (str): Word to write (must be signed four-digit decimal)
        """
        if isinstance(word, int):
            word = self.int_to_word(word)

        self.validate_address(address)
        self.validate_word(word)
        self.memory[address] = word

    def clear(self):
        """Reset all memory locations to +0000."""
        self.memory = ["+0000"] * self.size

    def __str__(self):
        """Return a string representation of the memory contents.

        Returns:
        str: Formatted string showing memory contents with row and column numbers
        """
        # Create column header
        output = ["            ", " ".join(f"{i:02d}       " for i in range(10)), "\n"]

        # Create memory contents with row numbers
        for i in range(0, self.size, 10):
            row = f"{i:02d} "
            row += " ".join(self.memory[i : i + 10])
            output.append(row + "\n")

        return "".join(output).rstrip()

    @staticmethod
    def word_to_int(word):
        """Convert a word to its integer representation.

        Parameters:
        word (str): Word to convert

        Returns:
        int: Integer representation of the word
        """
        Memory.validate_word(word)
        return int(word)

    @staticmethod
    def int_to_word(number):
        """Convert an integer to a valid word format.

        Parameters:
        number (int): Number to convert

        Returns:
        str: Word representation of the number

        Raises:
        ValueError: If number is out of valid range
        """
        if not (-9999 <= number <= 9999):
            raise ValueError("Number out of range (-9999 to 9999)")

        sign = "+" if number >= 0 else "-"
        return f"{sign}{abs(number):04d}"
