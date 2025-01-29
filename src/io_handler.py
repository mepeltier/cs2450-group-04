class IOHandler:
    def __init__(self, log_file=None):
        """
        Initializes the IOHandler.
        
        Parameters:
        log_file (str, optional): Path to a log file for logging outputs. Defaults to None.
        """
        self.log_file = log_file

    def read_int(self, text):
        """
        Prompts the user to enter a signed four-digit integer.
        
        Parameters:
        text (str): The prompt message displayed to the user.
        
        Returns:
        int: A valid integer in the range -9999 to 9999.
        """
        while True:
            try:
                user_input = int(input(text))
                if -9999 <= user_input <= 9999:
                    return user_input
                else:
                    print("Invalid input. Please enter a number between -9999 and 9999.")
            except ValueError:
                print("Invalid input. Please enter a valid signed four-digit number.")

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
