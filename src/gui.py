'''Class to handle the GUI'''

import sys
import tkinter as tk
from tkinter import *
from termcolor import colored
import difflib
from tkinter import filedialog, messagebox, ttk, font

class PrintRedir:
    def __init__(self, txt):
        self.text_space = txt

    def write(self, string):
        self.text_space.insert("1.0", string)
        self.text_space.see(tk.END)

    def flush(self):
        pass

class ColoredText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag_configure("green", foreground="green")
        self.tag_configure("left", justify="left")  # Left justification configuration

    def insert_colored_text(self, text):
        parts = self.split_text_with_colors(text)
        for part, color in parts:
            if color:
                self.insert(tk.END, part, color)
            else:
                self.insert(tk.END, part)

    def split_text_with_colors(self, text):
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
    def __init__(self, boot, InitWithFileLoaded=None):
        self.root = tk.Tk()
        self.root.title("UVSim - BasicML Simulator")
        self.root.geometry('833x519')
        self.root.minsize(833, 519)
        self.root.iconbitmap('cpu.ico')
        
        # Configure root grid weights
        self.root.grid_columnconfigure(0, weight=0)  # Remove weight from left column
        self.root.grid_columnconfigure(1, weight=1)  # Make main frame take all extra space
        self.root.grid_rowconfigure(0, weight=1)

        self.boot = boot
        self.io = boot.io
        self.mem = boot.memory
        self.cpu = boot.cpu

        style = ttk.Style(self.root)
        style.configure("TButton", font=("Arial", 8))
        style.configure("TLabel", font=("Arial", 12, "bold"))
        style.configure("TSeperator", font=("Arial", 14, "bold"))

        # Declare and Place Section Framing
        prog_input_frame = ttk.Frame(self.root, padding=10)
        main_frame = ttk.Frame(self.root, padding=10)

        #prog_input_frame.columnconfigure((0, 1), weight=1, uniform='a')
        #prog_input_frame.rowconfigure((0, 1, 2), weight=1, uniform='a')

        prog_input_frame.grid(row=0, column=0, sticky="ns")
        main_frame.grid(row=0, column=1, sticky=NSEW)

        # Configure prog_input_frame grid weights
        prog_input_frame.grid_rowconfigure(3, weight=1)  # Make row with program_text expandable
        prog_input_frame.grid_columnconfigure((0, 1), weight=1)  # Make columns equal width

        # Declare and Place Program Input Frame, buttons, and opcode textbox
        load_file_btn = ttk.Button(prog_input_frame, text="Load File", command=self.load_file, padding=5)
        clear_btn = ttk.Button(prog_input_frame, text="Clear", command=self.clear_program, padding=5)
        load_mem_btn = ttk.Button(prog_input_frame, text="Load Into Memory", command=self.load_memory, padding=5)
        self.program_text = tk.Text(prog_input_frame, height=25, width=20)

        load_file_btn.grid(column=0, row=0, padx=3, pady=3, sticky="ew")
        clear_btn.grid(column=1, row=0, padx=3, pady=3, sticky="ew")
        load_mem_btn.grid(column=0, row=2, columnspan=2, padx=3, pady=3, sticky="ew")
        self.program_text.grid(column=0, row=3, columnspan=2, padx=5, pady=5, sticky="nsew")


        # Configure main_frame grid weights
        main_frame.grid_rowconfigure(1, weight=1)  # Make memory frame expandable
        main_frame.grid_columnconfigure(0, weight=1)

        # Declare and Place Text box for Instructions
        inst_frame = ttk.Frame(main_frame, padding=10)
        self.instructions = tk.Entry(inst_frame, width=20, font=("Consolas", 40))
        self.instructions.grid(row=0, column=0, sticky="ew")
        inst_frame.grid(row=0, column=0, sticky="new")  # Stick to top

        # Configure inst_frame to expand horizontally
        inst_frame.grid_columnconfigure(0, weight=1)  # Allow the instruction frame to expand

        # Declare CPU Info Frame, Status label and Memory Display text in Memory Frame
        memory_frame = tk.Frame(main_frame, padx=10, pady=10)
        memory_frame.grid(row=1, column=0, sticky="nsew")  # Make memory_frame expandable

        # Configure grid weights for memory_frame
        memory_frame.grid_rowconfigure(2, weight=1)  # Make the row with memory_text expandable

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
        #self.memory_text = tk.Text(memory_frame, height=11, width=64, font=("Consolas", 12), wrap=NONE, state=tk.DISABLED)
        self.memory_text = ColoredText(memory_frame, height=11, width=64, font=("Consolas", 12), wrap=NONE, state=tk.DISABLED)
        self.memory_text.tag_configure("left", justify="left")
        
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

        # Configure memory_frame to expand horizontally
        memory_frame.grid_columnconfigure(0, weight=1)  # Allow the memory text to expand

        # Update memory text to expand
        self.memory_text.grid(row=2, column=0, columnspan=9, sticky="nsew")  # Ensure it fills the space

        # Initialize memory display with initial memory data and disable input
        self.memory_text.config(state=tk.NORMAL)
        self.memory_text.insert("1.0", " " + self.mem.__str__(), "center")  # Use "center" tag for centering
        self.memory_text.tag_add("center", "1.0", "end")  # Center the text
        self.memory_text.config(state=tk.DISABLED)

        self.memory_text.bind("<Configure>", self.adjust_memory_font_size)
        self.adjust_memory_font_size()
        
        # Declare and Place run, step, halt, reset buttons, and I/O text in Control Frame
        control_frame = ttk.Frame(main_frame, padding=10)

        run_btn = ttk.Button(control_frame, text="Run", command=self.run_program, padding=5)
        step_btn = ttk.Button(control_frame, text="Step", command=self.step_program, padding=5)
        halt_btn = ttk.Button(control_frame, text="Halt", command=self.halt_program, padding=5)
        reset_btn = ttk.Button(control_frame, text="Reset", command=self.reset_program, padding=5)
        self.io_text = tk.Text(control_frame, height=5, width=48)

        control_frame.grid(row=2, column=0, sticky="sew")  # Stick to bottom

        run_btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        step_btn.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        halt_btn.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        reset_btn.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.io_text.grid(row=0, column=2, rowspan=2, padx=5, pady=5, sticky="nsew")

        # Configure control_frame to expand horizontally
        control_frame.grid_columnconfigure(2, weight=1)  # Allow the I/O text to expand

        if InitWithFileLoaded:
            self.load_file(InitWithFileLoaded)
        
        self.root.mainloop()

    def load_file(self, file_path=None):
        if not file_path:
            file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if self.program_text.get("1.0", tk.END).strip() != "":
            self.program_text.insert(tk.END, "\n")

        try:
            with open(file_path, "r") as file:
                self.program_text.insert(tk.END, file.read())
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"File not found: {file_path}")
            return
    
    def clear_program(self):
        self.program_text.delete("1.0", tk.END)

    def load_memory(self):
        text = self.program_text.get("1.0", tk.END).splitlines()
        self.mem.clear()
        for addr, instruction in enumerate(text):
            try:
                self.mem.write(addr, instruction.strip())
            except IndexError:
                messagebox.showerror("Error", f"Invalid address: {addr}")
                return
            except ValueError:
                messagebox.showerror("Error", f"Invalid instruction: {instruction}")
                return
        self.update_memory_text()

    def adjust_memory_font_size(self, event=None):
        """Dynamically adjusts font size to fit text within memory_text widget with some padding."""
        self.memory_text.config(state=tk.NORMAL)  # Temporarily enable editing

        text = self.memory_text.get("1.0", "end-1c").strip()
        if not text:
            return  # Avoid errors when text is empty

        # Get widget dimensions
        widget_width = self.memory_text.winfo_width() * 0.95  # 5% padding on width
        widget_height = self.memory_text.winfo_height() * 0.95  # 5% padding on height
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


    def update_memory_text(self):
        self.memory_text.config(state=tk.NORMAL)
        self.memory_text.delete("1.0", tk.END)
        self.memory_text.insert_colored_text(" " + colored(self.mem.__str__(), "green"))
        self.memory_text.tag_add("left", "1.0", "end")  # Add left justification tag
        self.memory_text.config(state=tk.DISABLED)
        self.pc_label.config(text=str(self.cpu.pointer))
        self.acc_label.config(text=str(self.cpu.accumulator))

    def run_program(self):
        redir = PrintRedir(self.memory_text)
        sys.stdout = redir
        try:
            self.boot.run()
            self.status_label.config(text="Status: Program Executed")
            self.update_memory_text()
        except Exception as e:
            messagebox.showerror("Runtime Error", str(e))
    
    def step_program(self):
        messagebox.showinfo("Step", "Step functionality not implemented yet.")
    
    def halt_program(self):
        messagebox.showinfo("Halt", "Halt functionality not implemented yet.")
    
    def reset_program(self):
        self.mem.clear()
        self.cpu.boot_up()
        self.update_memory_text()
        self.status_label.config(text="Status: Reset")
