'''Class to handle the GUI'''

import sys
import tkinter as tk
from tkinter import *
from termcolor import colored
import difflib
from tkinter import filedialog, messagebox, ttk

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
        
        self.boot = boot
        self.io = boot.io
        self.mem = boot.memory
        self.cpu = boot.cpu

        style = ttk.Style(self.root)
        style.configure("TButton", font=("Arial", 8))
        style.configure("TLabel", font=("Arial", 12, "bold"))
        #style.configure("TFrame", font=("Arial", 12))
        style.configure("TSeperator", font=("Arial", 14, "bold"))

        # Declare and Place Section Framing
        prog_input_frame = ttk.Frame(self.root, padding=10)
        main_frame = ttk.Frame(self.root, padding=10)

        #prog_input_frame.columnconfigure((0, 1), weight=1, uniform='a')
        #prog_input_frame.rowconfigure((0, 1, 2), weight=1, uniform='a')

        prog_input_frame.grid(row=0, column=0, sticky=NSEW)
        main_frame.grid(row=0, column=1, sticky=NSEW)


        # Declare and Place Program Input Frame, buttons, and opcode textbox
        load_file_btn = ttk.Button(prog_input_frame, text="Load File", command=self.load_file, padding=5)
        clear_btn = ttk.Button(prog_input_frame, text="Clear", command=self.clear_program, padding=5)
        load_mem_btn = ttk.Button(prog_input_frame, text="Load Into Memory", command=self.load_memory, padding=5)
        self.program_text = tk.Text(prog_input_frame, height=25, width=20)

        load_file_btn.grid(column=0, row=0, padx=5, pady=5, sticky=NW)
        clear_btn.grid(column=1, row=0, padx=5, pady=5, sticky=NE)
        load_mem_btn.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky=NSEW)
        self.program_text.grid(column=0, row=3, columnspan=2, padx=5, pady=5, sticky=NSEW)


        # Declare and Place Text box for Instructions and tooltips in Instructions Frame
        inst_frame = ttk.Frame(main_frame, padding=10)
        #inst_img = PhotoImage(file="Rounded Textbox.png")
        #inst_label = ttk.Label(inst_frame, image=inst_img, border=0)
        self.instructions = tk.Entry(inst_frame, width=20, font=("Consolas", 40))
        self.instructions.grid(row=0, column=0)
        inst_frame.grid(row=0, column=0, sticky=NSEW)
        #inst_label.grid(row=0, column=0, sticky=EW)


        # Declare CPU Info Frame, Status label and Memory Display text in Memory Frame
        memory_frame = tk.Frame(main_frame, padx=10, pady=10)

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
        self.memory_text.tag_configure("center", justify="center")
        
        # Place Memory Frame and its components
        memory_frame.grid(row=1, column=0, sticky=EW)

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
        self.memory_text.grid(row=1, column=0, columnspan=9, sticky=EW)


        # Initialize memory display with initial memory data and disable input
        self.memory_text.config(state=tk.NORMAL)
        self.memory_text.insert("1.0", " " + self.mem.__str__())
        self.memory_text.tag_add("center", "1.0", "end")
        self.memory_text.config(state=tk.DISABLED)


        # Declare and Place run, step, halt, reset buttons, and I/O text in Control Frame
        control_frame = ttk.Frame(main_frame, padding=10)

        run_btn = ttk.Button(control_frame, text="Run", command=self.run_program, padding=5)
        step_btn = ttk.Button(control_frame, text="Step", command=self.step_program, padding=5)
        halt_btn = ttk.Button(control_frame, text="Halt", command=self.halt_program, padding=5)
        reset_btn = ttk.Button(control_frame, text="Reset", command=self.reset_program, padding=5)
        self.io_text = tk.Text(control_frame, height=5, width=48)

        control_frame.grid(row=2, column=0, sticky=NSEW)

        run_btn.grid(row=0, column=0, padx=5, sticky=NW)
        step_btn.grid(row=0, column=1, padx=5, sticky=NE)
        halt_btn.grid(row=1, column=0, padx=5, sticky=SW)
        reset_btn.grid(row=1, column=1, padx=5, sticky=SE)
        self.io_text.grid(row=1, column=2, columnspan=3, padx=5, pady=5, sticky=NSEW)

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

    def update_memory_text(self):
        self.memory_text.config(state=tk.NORMAL)
        self.memory_text.delete("1.0", tk.END)
        self.memory_text.insert_colored_text(" " + colored(self.mem.__str__(), "green"))
        self.memory_text.tag_add("center", "1.0", "end")
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
