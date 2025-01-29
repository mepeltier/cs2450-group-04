class IOHandler:
    def __init__(self, log_file=None):
        self.log_file = log_file

    def read_int(self, text):
        """
        Reads a signed four-digit decimal number from user input.
        Ensures that the input is a valid integer within the range -9999 to 9999.
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
        Prints the given value to the console or logs it to a file based on the log flag.
        """
        if log and self.log_file:
            with open(self.log_file, "a") as log_file:
                log_file.write(str(value) + "\n")
        else:
            print(value)

    def write_inline(self, value, log=False):
        """
        Prints the given value without a newline or logs it to a file based on the log flag.
        """
        if log and self.log_file:
            with open(self.log_file, "a") as log_file:
                log_file.write(str(value))
        else:
            print(value, end='')

    def read_choice(self, text, choices):
        """
        Reads a choice input from the user based on a given dictionary of choices.
        Displays all choices in a readable format before prompting input.
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

if __name__ == "__main__":
    print("This is a test")
    io_handler = IOHandler(log_file="uvsim.log")

    user_int = io_handler.read_int("Input a number: ")
    io_handler.write(f"You entered: {user_int}")
    
    choices = {"1": "Continue", "2": "Exit"}
    choice = io_handler.read_choice("Select an option:", choices)
    io_handler.write(f"You selected: {choices[choice]}")
