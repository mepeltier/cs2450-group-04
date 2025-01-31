class IOHandler:
    def __init__(self, log_file=None):
        """
        Initializes the IOHandler.
        
        Parameters:
        log_file (str, optional): Path to a log file for logging outputs. Defaults to None.
        """
        self.log_file = log_file

    def read_number(self, text, min_value, max_value):
        """
        Prompts the user to enter a number within a specific range.
        
        Parameters:
        text (str): The prompt message displayed to the user.
        min_value (int/float): The minimum acceptable value.
        max_value (int/float): The maximum acceptable value.

        Returns:
        int/float: A valid number within the specified range.
        """
        while True:
            try:
                user_input = float(input(text))  # Allows decimals if needed
                if min_value <= user_input <= max_value:
                    return user_input
                else:
                    print(f"Invalid input. Please enter a number between {min_value} and {max_value}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def read_operation(self, text):
        """
        Prompts the user to enter a signed four-digit integer.
        
        Parameters:
        text (str): The prompt message displayed to the user.
        
        Returns:
        int: A valid integer in the range 1000 to 9999.
        """
        return self.read_number(text, 1000, 9999)

    def write(self, value, log=False):
        """
        Outputs a message to the console or logs it to a file.
        
        Parameters:
        value (str): The message to be displayed or logged.
        log (bool, optional): If True, logs to file instead of printing. Defaults to False.
        """
        if log and self.log_file:
            with open(self.log_file, "a") as log_file:
                log_file.write(str(value) + "\n")
        else:
            print(value)

    def write_inline(self, value, log=False):
        """
        Outputs a message without a newline or logs it to a file.
        
        Parameters:
        value (str): The message to be displayed or logged.
        log (bool, optional): If True, logs to file instead of printing. Defaults to False.
        """
        if log and self.log_file:
            with open(self.log_file, "a") as log_file:
                log_file.write(str(value))
        else:
            print(value, end='')

    def read_choice(self, text, choices):
        """
        Prompts the user to select an option from a given dictionary of choices.
        
        Parameters:
        text (str): The prompt message displayed to the user.
        choices (dict): A dictionary mapping valid input keys to their descriptions.
        
        Returns:
        str: The key corresponding to the user's valid selection.
        """
        while True:
            print(text)
            for key, value in choices.items():
                print(f"{key}: {value}")
            user_input = input("Enter your choice: ").strip()
            if user_input in choices:
                return user_input
            else:
                print("Invalid choice. Please select a valid option.")

    def read_yes_no(self, text):
        """
        Prompts the user to confirm a Yes or No input.

        Parameters:
        text (str): The prompt message displayed to the user.

        Returns:
        bool: True if the user selects 'yes', False if 'no'.
        """
        while True:
            user_input = input(f"{text} (yes/no): ").strip().lower()
            if user_input in ['yes', 'y']:
                return True
            elif user_input in ['no', 'n']:
                return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    def read_string(self, text, min_length=1, max_length=50):
        """
        Prompts the user to enter a string with length constraints.

        Parameters:
        text (str): The prompt message displayed to the user.
        min_length (int): Minimum length of the string.
        max_length (int): Maximum length of the string.

        Returns:
        str: A valid string within the length constraints.
        """
        while True:
            user_input = input(text).strip()
            if min_length <= len(user_input) <= max_length:
                return user_input
            else:
                print(f"Invalid input. Please enter a string between {min_length} and {max_length} characters.")

    def read_from_file(self, file_path):
        """
        Reads input from a file and returns it as a list of lines.

        Parameters:
        file_path (str): The path to the input file.

        Returns:
        list: A list of strings, each representing a line of input from the file.
        """
        try:
            with open(file_path, "r") as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            return []
