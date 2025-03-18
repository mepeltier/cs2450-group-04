'''Class to handle the GUI'''

import textwrap
import tkinter as tk
from tkinter import *
from termcolor import colored
from tkinter import filedialog, messagebox, ttk, font

        
class ColoredText(tk.Text):
    '''Class to handle colored text from termcolor in the GUI'''
    def __init__(self, *args, **kwargs):
        '''Initialize the ColoredText class to inherit from the Text tkinter class'''
        super().__init__(*args, **kwargs)
        self.tag_configure("green", foreground="green")
        self.tag_configure("center", justify="center")  # Left justification configuration

    def insert_colored_text(self, text):
        '''Insert colored text into the text widget'''
        parts = self.split_text_with_colors(text)
        for part, color in parts:
            if color:
                self.insert(tk.END, part, color)
            else:
                self.insert(tk.END, part)

    def split_text_with_colors(self, text):
        '''Split the text with color codes'''
        parts = []
        current_part = ""
        current_color = None
        i = 0

        while i < len(text):
            if text[i:i+5] == "\x1b[32m":
                if current_part:
                    parts.append((current_part, current_color))
                current_part = ""
                current_color = "green"
                i += 5
            elif text[i:i+5] == "\x1b[0m":
                if current_part:
                    parts.append((current_part, current_color))
                current_part = ""
                current_color = None
                i += 5
            else:
                current_part += text[i]
                i += 1
        if current_part:
            parts.append((current_part, current_color))
        return parts

class App:
    '''GUI functionality'''
    def __init__(self, boot, InitWithFileLoaded=None):
        '''Initialize the GUI'''
        self.boot = boot
        self.mem = boot.memory
        self.cpu = boot.cpu

        self.setup_root()
        self.setup_menu_bar()

        # Configure root grid weights
        self.root.grid_columnconfigure(0, weight=0)  # Remove weight from left column
        self.root.grid_columnconfigure(1, weight=1)  # Make main frame take all extra space
        self.root.grid_rowconfigure(0, weight=1)

        # Configure Style
        style = ttk.Style(self.root)
        style.theme_use("alt")

        self.setup_program_frame()
        self.setup_main_frame()

        # Check if a file was passed as an argument and load to program_text
        if InitWithFileLoaded:
            self.load_file(InitWithFileLoaded)
        
        self.root.mainloop()
    
    def setup_root(self):
        '''Sets up the root behavior of the window'''
        self.root = tk.Tk()
        self.root.title("UVSim - BasicML Simulator")
        self.root.geometry('960x552')
        self.root.minsize(960, 552)
        self.root.iconbitmap('gui/cpu.ico')
    
    def setup_menu_bar(self):
        '''Sets up the menu bar and its behavior'''
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.load_file)  # Add open file option
        filemenu.add_command(label="Clear", command=self.clear_program)  # Add clear program option
        filemenu.add_command(label="Exit", command=self.root.quit)  # Add exit option
        menubar.add_cascade(label="File", menu=filemenu)  # Add file menu to menubar

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Instructions Set", command=self.instructions_window)
        helpmenu.add_command(label="About", command=lambda: messagebox.showinfo("About", "UVSim - BasicML Simulator\n\nVersion 2.0\n"))
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)
    
    def setup_program_frame(self):
        '''Sets up the program frame, the area for loading in and editing the program'''
        # Declare and Place Program Framing
        prog_input_frame = ttk.Frame(self.root, padding=10)
        prog_input_frame.grid(row=0, column=0, sticky="ns") # Sticks to the top left

        # Configure prog_input_frame grid weights
        prog_input_frame.grid_rowconfigure(3, weight=1)  # Make row with program_text expandable
        prog_input_frame.grid_columnconfigure((0, 1), weight=0)  # Make columns equal width

        # Declare and Place Program Input Frame, Scrollbar, buttons, and opcode textbox
        load_file_btn = ttk.Button(prog_input_frame, text="Load File", command=self.load_file, padding=5)
        clear_btn = ttk.Button(prog_input_frame, text="Clear", command=self.clear_program, padding=5)
        load_mem_btn = ttk.Button(prog_input_frame, text="Load Into Memory", command=self.load_memory, padding=5)
        self.program_text = tk.Text(prog_input_frame, height=25, width=10)
        scrollbar = ttk.Scrollbar(prog_input_frame, orient=VERTICAL, command=self.program_text.yview)
        self.program_text.config(font=("Consolas", 25), yscrollcommand=scrollbar.set)  # Increase text font size and add scrollbar

        load_file_btn.grid(column=0, row=0, padx=3, pady=3, sticky="ew")
        clear_btn.grid(column=1, row=0, padx=3, pady=3, sticky="ew")
        load_mem_btn.grid(column=0, row=2, columnspan=2, padx=3, pady=3, sticky="ew")
        self.program_text.grid(column=0, row=3, columnspan=2, padx=5, pady=5, sticky="nsew")
        scrollbar.grid(column=2, row=3, pady=5, sticky="ns")

    def setup_main_frame(self):
        '''Sets up the main frame of the program. Including the instruction frame, memory frame, and control frame'''
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=1, sticky=NSEW) # Expands to fill the right

        # Configure main_frame grid weights
        main_frame.grid_rowconfigure(1, weight=1)  # Make memory frame expandable
        main_frame.grid_columnconfigure(0, weight=1)
        
        self.setup_instruction_frame(main_frame)
        self.setup_memory_frame(main_frame)
        self.setup_control_frame(main_frame)


    def setup_instruction_frame(self, main_frame):
        '''Sets up the instruction frame for providing information to the user'''
        # Declare and Place Text box for Instructions
        inst_frame = tk.Frame(main_frame, padx=10, pady=10)
        # Configure inst_frame to expand horizontally
        inst_frame.grid_columnconfigure(0, weight=1)

        self.instructions = tk.Label(inst_frame, text="Instruction", font=("Consolas", 11), anchor="center", height=3, wraplength=550)
        inst_frame.grid(row=0, column=0, sticky="new")  # Stick to top
        self.instructions.grid(row=0, column=0, sticky="ew", ipady=24)  # Center the label

        seperator = ttk.Separator(inst_frame, orient=HORIZONTAL)
        seperator.grid(row=1, column=0, columnspan=3, sticky="ew") # Add a separator

    def setup_memory_frame(self, main_frame):
        '''Sets up the memory frame, containing the the memory information. Ensuring the memory text resizes when the window changes.'''
        # Declare CPU Info Frame, Status label and Memory Display text in Memory Frame
        memory_frame = tk.Frame(main_frame, padx=10, pady=10)
        memory_frame.grid(row=1, column=0, sticky="nsew")  # Make memory_frame expandable

        # Configure grid weights for memory_frame
        memory_frame.grid_rowconfigure(2, weight=1)  # Make the row with memory_text expandable
        memory_frame.grid_columnconfigure(0, weight=1)  # Allow the memory  to expand


        # Place CPU info labels at the top of the memory_frame
        memory_label = ttk.Label(memory_frame, text="Memory")
        boldseperator = ttk.Separator(memory_frame, orient=VERTICAL)
        pc_frame = ttk.Label(memory_frame, text="PC:")
        self.pc_label = ttk.Label(memory_frame, text="00")
        seperator1 = ttk.Separator(memory_frame, orient=VERTICAL)
        acc_frame = ttk.Label(memory_frame, text="Accumulator:")
        self.acc_label = ttk.Label(memory_frame, text="+0000")
        seperator2 = ttk.Separator(memory_frame, orient=VERTICAL)
        self.status_label = ttk.Label(memory_frame, text="Status: Ready", relief=tk.SUNKEN, anchor=tk.W)
        boldseperator1 = ttk.Separator(memory_frame, orient=HORIZONTAL)
        self.memory_text = ColoredText(memory_frame, height=11, width=64, font=("Courier", 12), wrap=NONE, state=tk.DISABLED)
        self.memory_text.tag_configure("center", justify="center")
        
        # Place Memory Frame and its components
        memory_label.grid(row=0, column=0, sticky=W)
        boldseperator.grid(row=0, column=1, sticky=NS)
        pc_frame.grid(row=0, column=2)
        self.pc_label.grid(row=0, column=3)
        seperator1.grid(row=0, column=4, sticky=NS)
        acc_frame.grid(row=0, column=5)
        self.acc_label.grid(row=0, column=6)
        seperator2.grid(row=0, column=7, sticky=NS)
        self.status_label.grid(row=0, column=8, sticky=EW)
        boldseperator1.grid(row=1, column=0, columnspan=9, sticky=EW)

        # Update memory text to expand
        self.memory_text.grid(row=2, column=0, columnspan=9, sticky="nsew")  # Ensure it fills the space

        # Initialize memory display with initial memory data and disable input
        self.memory_text.config(state=tk.NORMAL)
        self.update_memory_text(self.mem.__str__())
        self.memory_text.tag_add("center", "1.0", "end")  # Center the rest of the text
        self.memory_text.config(state=tk.DISABLED)
        self.memory_text.bind("<Configure>", self.adjust_memory_font_size) # Binds the adjust memory font size when window is changed

    def setup_control_frame(self, main_frame):
        '''Sets up the control frame for controlling the program'''
        # Declare and Place run, step, halt, reset buttons, and I/O text in Control Frame
        control_frame = ttk.Frame(main_frame, padding=10)
        control_frame.grid_columnconfigure(2, weight=1)  # Allow the I/O to expand horizontally

        run_btn = ttk.Button(control_frame, text="Run", command=self.run_program, padding=5)
        step_btn = ttk.Button(control_frame, text="Step", command=self.step_program, padding=5)
        halt_btn = ttk.Button(control_frame, text="Halt", command=self.halt_program, padding=5)
        reset_btn = ttk.Button(control_frame, text="Reset", command=self.reset_program, padding=5)
        seperator3 = ttk.Separator(control_frame, orient=VERTICAL)
        self.io_label = ttk.Label(control_frame, text="I/O", font=("Consolas", 11))
        self.io_text = ttk.Entry(control_frame, font=("Consolas", 25), state=tk.DISABLED)

        control_frame.grid(row=2, column=0, sticky="sew")  # Stick to bottom

        run_btn.grid(row=0, rowspan=2, column=0, padx=5, pady=5, sticky="w")
        step_btn.grid(row=0, rowspan=2, column=1, padx=5, pady=5, sticky="w")
        halt_btn.grid(row=2, rowspan=2, column=0, padx=5, pady=5, sticky="w")
        reset_btn.grid(row=2, rowspan=2, column=1, padx=5, pady=5, sticky="w")
        seperator3.grid(row=0, rowspan=4, column=2, sticky="nsw")
        self.io_label.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.io_text.grid(row=1, rowspan=3, column=2, padx=5, pady=5, sticky="ew")


    def load_file(self, file_path=None):
        '''Load a file into the program_text widget'''
        if not file_path:
            file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if self.program_text.get("1.0", tk.END).strip() != "":
            self.program_text.insert(tk.END, "\n")

        try:
            with open(file_path, "r") as file:
                self.program_text.insert(tk.END, file.read())
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"File not found: {file_path}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
            return
        self.status_label.config(text="Status: Ready")
    
    def clear_program(self):
        '''Clear the program_text widget'''
        self.program_text.delete("1.0", tk.END)

    def load_memory(self):
        '''Load the program_text widget contents into memory'''
        text = self.program_text.get("1.0", tk.END).splitlines()
        self.mem.clear()
        for addr, instruction in enumerate(text):
            if instruction.strip() == "":
                addr -= 1
                continue
            elif instruction.strip().__len__() > 5:
                self.mem.write(addr, instruction[0:5])
                continue

            try:
                self.mem.write(addr, instruction.strip())
            except IndexError:
                messagebox.showerror("Error", f"Invalid address: {addr}")
                return
            except ValueError:
                messagebox.showerror("Error", f"Invalid instruction: {instruction}")
                return
        self.status_label.config(text="Status: Ready")
        self.update_memory_text()

    def adjust_memory_font_size(self, event=None):
        '''Dynamically adjusts font size to fit text within memory_text widget with some padding.'''
        self.memory_text.config(state=tk.NORMAL)  # Temporarily enable editing

        text = self.memory_text.get("1.0", "end-1c").strip()
        if not text:
            return  # Avoid errors when text is empty

        # Get widget dimensions
        widget_width = self.memory_text.winfo_width() * 0.97  # 3% padding on width
        widget_height = self.memory_text.winfo_height() * 0.97  # 3% padding on height
        new_size = 8  # Start with a base font size

        # Create a temporary font object
        text_font = font.Font(family="Consolas", size=new_size)
        
        while True:
            # Calculate text width & height with the current font size
            text_width = max(text_font.measure(line) for line in text.split("\n"))  # Widest line
            text_height = text_font.metrics("linespace") * len(text.split("\n"))  # Total height

            # If text fits within the widget (with padding), increase size, otherwise stop
            if text_width < widget_width and text_height < widget_height:
                new_size += 1
                text_font = font.Font(family="Consolas", size=new_size)
            else:
                new_size -= 1  # Step back to the last working size
                break

        # Apply the adjusted font size
        self.memory_text.config(font=("Consolas", new_size), state=tk.DISABLED)

    def update_memory_text(self, text=None):
        '''Update the memory_text widget with the current memory contents and highlights the pc'''
        pc = self.cpu.pointer

        self.memory_text.config(state=tk.NORMAL)
        self.memory_text.delete("1.0", tk.END)

        # Get the current memory lines as a list
        if not text:
            text = self.mem.__str__()
        
        first_line = text.splitlines()[0]  # Get the first line
        memory_lines = text.splitlines()[1:] # Get the rest of the lines
        
        # Insert the first line with left alignment
        self.memory_text.insert_colored_text(" " + first_line + "\n")

        for i, line in enumerate(memory_lines):
            instructions = line.split()  # Split the line into individual instructions
            for j, instruction in enumerate(instructions):
                if i * len(instructions) + j == pc + 1:
                    self.memory_text.insert_colored_text(colored(instruction + " ", "green"))
                    # Display the current instruction in the instructions label
                    try:
                        self.instructions.config(text=f"{self.cpu.operation(self.mem.word_to_int(instruction), self, True)}")
                    except:
                        self.instructions.config(text="Instruction")
                else:
                    self.memory_text.insert_colored_text(instruction + " ")
            if not line[0:2] == "90": # Don't add a newline if it is the last line
                self.memory_text.insert_colored_text("\n")
            
        self.memory_text.tag_add("center", "1.0", "end")
        self.memory_text.config(state=tk.DISABLED)
        self.pc_label.config(text=str(self.cpu.pointer))
        self.acc_label.config(text=str(self.cpu.accumulator))
        self.adjust_memory_font_size()

    def run_program(self):
        '''Run the program'''
        if self.cpu.halted and self.mem.read(self.cpu.pointer) in ("+4300", "-4300"): # Don't run if the program is halted and send a halt message
            messagebox.showinfo("Halted", "Program is halted")
            return
        elif self.cpu.halted and self.mem.read(self.cpu.pointer) == "+0000": # Don't run if the memory is empty
            return
        elif self.cpu.pointer > 0: # If the pointer is greater than 0, continue the program
            self.cpu.halted = False
            cont = True
        else: # Otherwise, reset the halt flag, start the program and reinitialize the cpu
            self.cpu.halted = False
            cont = False

        self.status_label.config(text="Status: Running")
            
        try:
            self.boot.run(self, cont)

        except Exception as e:
            messagebox.showerror("Runtime Error", str(e))

        self.update_memory_text()
        self.halt_program()
    
    def step_program(self):
        '''Step through the program'''
        if self.cpu.halted and self.mem.read(self.cpu.pointer) in ("+4300", "-4300"):
            messagebox.showinfo("Halted", "Program is halted")
            return
        elif self.cpu.halted and self.mem.read(self.cpu.pointer) == "+0000":
            return
        else:
            self.cpu.halted = False

        self.status_label.config(text="Status: Stepped")
        self.pc_label.config(text=str(self.cpu.pointer))
        self.acc_label.config(text=str(self.cpu.accumulator))

        try:
            operand = self.mem.word_to_int(self.mem.read(self.cpu.pointer))
            self.cpu.operation(operand, self)
            self.cpu.pointer += 1
        
        except Exception as e:
            messagebox.showerror("Runtime Error", str(e))

        self.update_memory_text()
        self.halt_program()

    def halt_program(self):
        '''Halt the program'''
        self.cpu.halted = True
        self.status_label.config(text="Status: Halted")
    
    def reset_program(self):
        '''Reset the program and reset labels and text widgets to default values'''
        self.cpu.halted = False
        self.mem.clear()
        self.io_label.config(text="I/O")
        self.io_text.config(state=tk.NORMAL)
        self.io_text.delete("0", tk.END)
        self.io_text.config(state=tk.DISABLED)
        self.cpu.boot_up()
        self.update_memory_text()
        self.status_label.config(text="Status: Reset")

    def instructions_window(self):
        '''Display the instructions set window'''
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("Instructions Set")
        instructions_window.geometry("1100x375")
        instructions_window.iconbitmap('gui/cpu.ico')
        instructions_window.minsize(1100, 375)
        instructions_label = tk.Label(instructions_window, text=textwrap.dedent('''
            I/O operation:
            READ = 10 Read a word from the keyboard into a specific location in memory.
            WRITE = 11 Write a word from a specific location in memory to screen.
                                                                                
            Load/store operations:
            LOAD = 20 Load a word from a specific location in memory into the accumulator.
            STORE = 21 Store a word from the accumulator into a specific location in memory.
                                                                                
            Arithmetic operation:
            ADD = 30 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
            SUBTRACT = 31 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
            DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
            MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).
                                                                                
            Control operation:
            BRANCH = 40 Branch to a specific location in memory
            BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative.
            BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero.
            HALT = 43 Pause the program
            '''), wraplength=1200, justify=LEFT, font=("Consolas", 11))
        instructions_label.pack(padx=10, pady=10)
