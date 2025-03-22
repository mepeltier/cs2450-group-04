'''Class to handle the GUI'''

import textwrap
import tkinter as tk
from tkinter import *
from termcolor import colored
from tkinter import filedialog, messagebox, ttk, font, colorchooser
import json
import os

class ColoredText(tk.Text):
    '''Class to handle colored text from termcolor in the GUI'''
    def __init__(self, *args, **kwargs):
        '''Initialize the ColoredText class to inherit from the Text tkinter class'''
        super().__init__(*args, **kwargs)
        self.tag_configure("primary", foreground=COLOR["primary_text"])
        self.tag_configure("secondary", foreground=COLOR["secondary_text"])
        self.tag_configure("center", justify="center") 

    def insert_colored_text(self, text, color=None):
        '''Insert colored text into the text widget'''
        if color:
            self.insert(tk.END, text, color)
        else:
            self.insert(tk.END, text)

    def set_colors(self, primary_color, secondary_color):
        '''Update the color tags with new colors'''
        self.tag_configure("primary", foreground=primary_color)
        self.tag_configure("secondary", foreground=secondary_color)

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

class ColorChooser:
    '''Custom color chooser dialog'''
    def __init__(self, parent):
        self.parent = parent
        self.dialog = None
        # Get current colors from parent (App instance)
        self.primary_color = parent.primary_color
        self.secondary_color = parent.secondary_color
        self.primary_text_color = parent.primary_text_color
        self.secondary_text_color = parent.secondary_text_color
        self.pc_text_color = parent.pc_text_color
        
    def adjust_color_for_hover(self, color, darken=True):
        '''Adjust color brightness for hover effect'''
        # Convert hex to RGB
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Adjust brightness
        factor = 0.9 if darken else 1.0
        new_rgb = tuple(int(c * factor) for c in rgb)
        
        # Convert back to hex
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)
    
    def on_enter(self, e, frame, original_color):
        '''Handle mouse enter event'''
        frame.configure(bg=self.adjust_color_for_hover(original_color, True))
    
    def on_leave(self, e, frame, original_color):
        '''Handle mouse leave event'''
        frame.configure(bg=original_color)
    
    def show(self):
        '''Display the color chooser dialog'''
        self.dialog = Toplevel(self.parent.root)  # Use parent.root as the Tkinter parent
        self.dialog.title("Customize Colors")
        self.dialog.geometry("400x250")  
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent.root)
        self.dialog.grab_set()
        
        # Configure dialog grid weights to allow button frame to stick to bottom
        self.dialog.grid_columnconfigure(0, weight=1)
        self.dialog.grid_rowconfigure(0, weight=1)
        self.dialog.grid_rowconfigure(1, weight=0)
        
        # Create main frame for color options
        main_frame = Frame(self.dialog, padx=20, pady=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Color picker sections - not using buttons due to  Mac OS X compatibility issues
        Label(main_frame, text="Primary Color:", anchor=W).grid(row=0, column=0, sticky=W, pady=5)
        self.primary_btn = Frame(main_frame, width=50, height=25,
                               relief=RAISED, borderwidth=2)
        self.primary_btn.grid(row=0, column=1, padx=10)
        self.primary_btn.bind('<Button-1>', lambda e: self.choose_color("primary"))
        self.primary_btn.bind('<Enter>', lambda e: self.on_enter(e, self.primary_btn, self.primary_color))
        self.primary_btn.bind('<Leave>', lambda e: self.on_leave(e, self.primary_btn, self.primary_color))
        self.primary_btn.grid_propagate(False)  # Prevent frame from shrinking
        
        self.primary_label = Label(main_frame, text=self.primary_color)
        self.primary_label.grid(row=0, column=2, sticky=W)
        
        Label(main_frame, text="Secondary Color:", anchor=W).grid(row=1, column=0, sticky=W, pady=5)
        self.secondary_btn = Frame(main_frame, width=50, height=25,
                                 relief=RAISED, borderwidth=2)
        self.secondary_btn.grid(row=1, column=1, padx=10)
        self.secondary_btn.bind('<Button-1>', lambda e: self.choose_color("secondary"))
        self.secondary_btn.bind('<Enter>', lambda e: self.on_enter(e, self.secondary_btn, self.secondary_color))
        self.secondary_btn.bind('<Leave>', lambda e: self.on_leave(e, self.secondary_btn, self.secondary_color))
        self.secondary_btn.grid_propagate(False)
        
        self.secondary_label = Label(main_frame, text=self.secondary_color)
        self.secondary_label.grid(row=1, column=2, sticky=W)
        
        Label(main_frame, text="Primary Text Color:", anchor=W).grid(row=2, column=0, sticky=W, pady=5)
        self.primary_text_btn = Frame(main_frame, width=50, height=25,
                                    relief=RAISED, borderwidth=2)
        self.primary_text_btn.grid(row=2, column=1, padx=10)
        self.primary_text_btn.bind('<Button-1>', lambda e: self.choose_color("primary_text"))
        self.primary_text_btn.bind('<Enter>', lambda e: self.on_enter(e, self.primary_text_btn, self.primary_text_color))
        self.primary_text_btn.bind('<Leave>', lambda e: self.on_leave(e, self.primary_text_btn, self.primary_text_color))
        self.primary_text_btn.grid_propagate(False)
        
        self.primary_text_label = Label(main_frame, text=self.primary_text_color)
        self.primary_text_label.grid(row=2, column=2, sticky=W)
        
        Label(main_frame, text="Secondary Text Color:", anchor=W).grid(row=3, column=0, sticky=W, pady=5)
        self.secondary_text_btn = Frame(main_frame, width=50, height=25,
                                      relief=RAISED, borderwidth=2)
        self.secondary_text_btn.grid(row=3, column=1, padx=10)
        self.secondary_text_btn.bind('<Button-1>', lambda e: self.choose_color("secondary_text"))
        self.secondary_text_btn.bind('<Enter>', lambda e: self.on_enter(e, self.secondary_text_btn, self.secondary_text_color))
        self.secondary_text_btn.bind('<Leave>', lambda e: self.on_leave(e, self.secondary_text_btn, self.secondary_text_color))
        self.secondary_text_btn.grid_propagate(False)
        
        self.secondary_text_label = Label(main_frame, text=self.secondary_text_color)
        self.secondary_text_label.grid(row=3, column=2, sticky=W)

        Label(main_frame, text="PC Text Color:", anchor=W).grid(row=4, column=0, sticky=W, pady=5)
        self.pc_text_btn = Frame(main_frame, width=50, height=25,
                                      relief=RAISED, borderwidth=2)
        self.pc_text_btn.grid(row=4, column=1, padx=10)
        self.pc_text_btn.bind('<Button-1>', lambda e: self.choose_color("pc_text"))
        self.pc_text_btn.bind('<Enter>', lambda e: self.on_enter(e, self.pc_text_btn, self.pc_text_color))
        self.pc_text_btn.bind('<Leave>', lambda e: self.on_leave(e, self.pc_text_btn, self.pc_text_color))
        self.pc_text_btn.grid_propagate(False)
        
        self.pc_text_label = Label(main_frame, text=self.pc_text_color)
        self.pc_text_label.grid(row=4, column=2, sticky=W)
        
        # Configure color displays
        self.update_button_colors()
        
        # Button frame - now placed at the bottom of the dialog using grid
        button_frame = Frame(self.dialog, padx=10, pady=10)
        button_frame.grid(row=1, column=0, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)  # Make buttons right-aligned
        
        # Button container for right alignment
        buttons_container = Frame(button_frame)
        buttons_container.grid(row=0, column=0, sticky="e")
        
        # Add Reset to Default button
        reset_btn = Button(buttons_container, text="Reset to Default", command=self.reset_to_default)
        reset_btn.pack(side=LEFT, padx=5)
        
        Button(buttons_container, text="Apply", command=self.apply_colors).pack(side=LEFT, padx=5)
        Button(buttons_container, text="Cancel", command=self.dialog.destroy).pack(side=LEFT, padx=5)
        
        # Center dialog on parent
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = self.parent.root.winfo_rootx() + (self.parent.root.winfo_width() - width) // 2
        y = self.parent.root.winfo_rooty() + (self.parent.root.winfo_height() - height) // 2
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        self.dialog.wait_window()
    
    def update_button_colors(self):
        '''Update all color display frames'''
        for color_type in ['primary', 'secondary', 'primary_text', 'secondary_text', 'pc_text']:
            color = getattr(self, f"{color_type}_color")
            frame = getattr(self, f"{color_type}_btn")
            frame.configure(bg=color)
    
    def choose_color(self, color_type):
        '''Open color picker and update the chosen color'''
        color = colorchooser.askcolor(initialcolor=getattr(self, f"{color_type}_color"))
        if color[1]:  # If color was chosen (not canceled)
            setattr(self, f"{color_type}_color", color[1])
            # Update frame color to display the selected color
            frame = getattr(self, f"{color_type}_btn")
            frame.configure(bg=color[1])
            # Update color value label
            getattr(self, f"{color_type}_label").config(text=color[1])
    
    def apply_colors(self):
        '''Apply the chosen colors to the main application'''
        # Update parent's colors
        self.parent.primary_color = self.primary_color
        self.parent.secondary_color = self.secondary_color
        self.parent.primary_text_color = self.primary_text_color
        self.parent.secondary_text_color = self.secondary_text_color
        self.parent.pc_text_color = self.pc_text_color
        
        # Apply colors to UI
        self.parent.apply_colors()
        self.dialog.destroy()

    def reset_to_default(self):
        '''Reset colors to default values'''
        # Set colors to default values
        self.primary_color = self.parent.default_primary_color
        self.secondary_color = self.parent.default_secondary_color
        self.primary_text_color = self.parent.default_primary_text_color
        self.secondary_text_color = self.parent.default_secondary_text_color
        self.pc_text_color = self.parent.default_pc_text_color
        
        # Update color displays
        self.update_button_colors()
        
        # Update color value labels
        self.primary_label.config(text=self.primary_color)
        self.secondary_label.config(text=self.secondary_color)
        self.primary_text_label.config(text=self.primary_text_color)
        self.secondary_text_label.config(text=self.secondary_text_color)
        self.pc_text_label.config(text=self.pc_text_color)

# Default color scheme
COLOR = {
            "primary" : "#4C721D",
            "secondary" : "#FFFFFF",
            "primary_text" : "#000000",
            "secondary_text" : "#505050",
            "darkened_color" : "#d0d0d0",
            "pc" : "#008000"
        }

# Default font scheme
FONT = {
            "header" : ("Consolas", 21, "bold"),
            "primary" : ("Consolas", 18),
            "secondary" : ("Consolas", 14),
}

class App:
    '''GUI functionality'''
    def __init__(self, boot, InitWithFileLoaded=None):
        '''Initialize the GUI'''
        self.boot = boot
        self.mem = boot.memory
        self.cpu = boot.cpu

        # Initialize default colors
        self.default_primary_color = COLOR["primary"]  # Dark green for backgrounds
        self.default_secondary_color = COLOR["secondary"]  # White accent
        self.default_primary_text_color = COLOR["primary_text"]  # Black for main text
        self.default_secondary_text_color = COLOR["secondary_text"]  # Dark gray for secondary text
        self.default_pc_text_color = COLOR["pc"]  # Green for PC text
        self.default_darkened_color = COLOR["darkened_color"]  # Darker gray for inactive frames
        
        # Set current colors to default
        self.primary_color = self.default_primary_color
        self.secondary_color = self.default_secondary_color
        self.primary_text_color = self.default_primary_text_color
        self.secondary_text_color = self.default_secondary_text_color
        self.pc_text_color = self.default_pc_text_color
        self.darkened_color = self.default_darkened_color
        

        self.setup_root()
        
        # Configure Style before building UI
        self.setup_styles()
        
        self.setup_menu_bar()

        # Configure root grid weights
        self.root.grid_columnconfigure(0, weight=0)  # Remove weight from left column
        self.root.grid_columnconfigure(1, weight=1)  # Make main frame take all extra space
        self.root.grid_rowconfigure(0, weight=1)

        self.program_frame = self.setup_program_frame()
        self.setup_main_frame()

        # Check if a file was passed as an argument and load to program_text
        if InitWithFileLoaded:
            self.load_file(InitWithFileLoaded)
        
        # Apply initial colors
        self.apply_colors()
        
        # Set initial frame states
        self.highlight_program_frame()
        
        self.root.mainloop()
    
    def setup_root(self):
        '''Sets up the root behavior of the window'''
        self.root = tk.Tk()
        self.root.title("UVSim - BasicML Simulator")
        self.root.geometry('1007x600')
        self.root.minsize(1007, 600)
        self.root.iconbitmap('gui/cpu.ico')
        
    
    def setup_menu_bar(self):
        '''Sets up the menu bar and its behavior'''
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.load_file)
        filemenu.add_command(label="Clear", command=self.clear_program)
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        appearancemenu = Menu(menubar, tearoff=0)
        appearancemenu.add_command(label="Customize Colors", command=self.open_color_dialog)
        menubar.add_cascade(label="Appearance", menu=appearancemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Instructions Set", command=self.instructions_window)
        helpmenu.add_command(label="About", command=lambda: messagebox.showinfo("About", "UVSim - BasicML Simulator\n\nVersion 2.0\n"))
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)
    
    def setup_program_frame(self):
        '''Sets up the program frame, the area for loading in and editing the program.
        Returns:
            ttk.Frame: The created program frame containing the program input area.
        '''

        # Add inner frame with secondary color
        prog_input_frame = ttk.Frame(self.root, style='Primary.TFrame', padding=10)
        prog_input_frame.grid(row=0, column=0, sticky="ns") # Sticks to the top left

        # Configure prog_input_frame grid weights
        prog_input_frame.grid_rowconfigure(2, weight=1)  # Make row with program_text expandable
        prog_input_frame.grid_columnconfigure((0, 1), weight=0)  # Make columns equal width

        # Declare and Place Program Input Frame, Scrollbar, buttons, and opcode textbox
        load_file_btn = ttk.Button(prog_input_frame, text="Load File", command=self.load_file, padding=5)
        clear_btn = ttk.Button(prog_input_frame, text="Clear", command=self.clear_program, padding=5)
        load_mem_btn = ttk.Button(prog_input_frame, text="Load Into Memory", command=self.load_memory, padding=5)
        self.program_text = tk.Text(prog_input_frame, width=10, font=FONT["primary"], wrap=NONE)
        scrollbar = ttk.Scrollbar(prog_input_frame, orient=VERTICAL, command=self.program_text.yview)
        # Add a small separator
        separator = ttk.Separator(prog_input_frame, orient=HORIZONTAL)
        save_prog_btn = ttk.Button(prog_input_frame, text="Save Program", command=self.save_file, padding=5)

        load_file_btn.grid(column=0, row=0, padx=3, pady=3, sticky="ew")
        clear_btn.grid(column=1, row=0, padx=3, pady=3, sticky="ew")
        load_mem_btn.grid(column=0, row=1, columnspan=2, padx=3, pady=3, sticky="ew")
        self.program_text.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky="nsew")
        scrollbar.grid(column=1, row=2, pady=5, sticky="nse")
        separator.grid(column=0, row=3, columnspan=2, padx=3, pady=5, sticky="ew")
        save_prog_btn.grid(column=0, row=4, columnspan=2, padx=5, pady=5, sticky="ew")

        self.program_text.config(yscrollcommand=scrollbar.set)  # Decreased font size per todos, fixed scrollbar to be inside the textbox

        return prog_input_frame

    def setup_main_frame(self):
        '''Sets up the main frame of the program. Including the instruction frame, memory frame, and control frame.
        Returns:
            ttk.Frame: The created main frame containing all program components.
        '''
        main_frame = ttk.Frame(self.root, style='Primary.TFrame')
        main_frame.grid(row=0, column=1, sticky=NSEW) # Expands to fill the right

        # Configure main_frame grid weights
        main_frame.grid_rowconfigure(1, weight=1)  # Make memory frame expandable
        main_frame.grid_columnconfigure(0, weight=1)
        
        self.instruction_frame = self.setup_instruction_frame(main_frame)
        self.memory_frame = self.setup_memory_frame(main_frame)
        self.control_frame = self.setup_control_frame(main_frame)

        return main_frame

    def setup_instruction_frame(self, main_frame):
        '''Sets up the instruction frame for providing information to the user.
        Args:
            main_frame (ttk.Frame): The parent frame to place the instruction frame in.
        Returns:
            ttk.Frame: The created instruction frame containing the instruction display.
        '''
        # Declare and Place Text box for Instructions
        inst_frame = ttk.Frame(main_frame, style='Primary.TFrame', padding=10)
        # Configure inst_frame to expand horizontally
        inst_frame.grid_columnconfigure(0, weight=1)

        # Use regular tk.Label for direct color control
        self.instructions = tk.Label(inst_frame, text="Instruction", 
                                   font=FONT["secondary"], anchor="center",
                                   bg=self.secondary_color, fg=self.primary_text_color, 
                                   wraplength=700, width=100, height=2) # Ensure instruction window doesn't resize when it is updated
        inst_frame.grid(row=0, column=0, sticky="new")  # Stick to top
        self.instructions.grid(row=0, column=0, sticky="ew", ipady=25)  # Center the label

        seperator = ttk.Separator(inst_frame, orient=HORIZONTAL)
        seperator.grid(row=1, column=0, sticky="ew", pady=(10, 0)) # Add a separator, ensure padding is set for top only to seperate it from the label

        return inst_frame

    def setup_memory_frame(self, main_frame):
        '''Sets up the memory frame, containing the the memory information. Ensuring the memory text resizes when the window changes.
        Args:
            main_frame (ttk.Frame): The parent frame to place the memory frame in.
        Returns:
            ttk.Frame: The created memory frame containing the memory display and CPU information.
        '''
        # Declare CPU Info Frame, Status label and Memory Display text in Memory Frame
        memory_frame = ttk.Frame(main_frame, style='Primary.TFrame', padding=10)
        memory_frame.grid(row=1, column=0, sticky="nsew")  # Make memory_frame expandable

        # Configure grid weights for memory_frame
        memory_frame.grid_rowconfigure(2, weight=1)  # Make the row with memory_text expandable
        memory_frame.grid_columnconfigure(0, weight=1)  # Allow the memory to expand

        # Place CPU info labels at the top of the memory_frame using regular labels
        self.memory_label = tk.Label(memory_frame, text="Memory", bg=self.primary_color, fg=self.primary_text_color, font=FONT["header"], padx=5)
        boldseperator = ttk.Separator(memory_frame, orient=VERTICAL)
        self.pc_frame = tk.Label(memory_frame, text="PC:", bg=self.secondary_color, fg=self.secondary_text_color, font=FONT["secondary"])
        self.pc_label = tk.Label(memory_frame, text="00", bg=self.secondary_color, fg=self.secondary_text_color, font=FONT["secondary"])
        seperator1 = ttk.Separator(memory_frame, orient=VERTICAL)
        self.acc_frame = tk.Label(memory_frame, text="Accumulator:", bg=self.secondary_color, fg=self.secondary_text_color, font=FONT["secondary"])
        self.acc_label = tk.Label(memory_frame, text="+0000", bg=self.secondary_color, fg=self.secondary_text_color, font=FONT["secondary"])
        seperator2 = ttk.Separator(memory_frame, orient=VERTICAL)
        self.status_label = tk.Label(memory_frame, text="Status: Ready", bg=self.secondary_color, fg=self.secondary_text_color, relief=tk.SUNKEN, anchor=tk.W, font=FONT["secondary"])
        boldseperator1 = ttk.Separator(memory_frame, orient=HORIZONTAL)
        self.memory_text = ColoredText(memory_frame, height=11, width=64, font=FONT["secondary"], wrap=NONE, state=tk.DISABLED)
        self.memory_text.tag_configure("center", justify="center")
        
        # Place Memory Frame and its components, ensuring they expand to fill the space
        self.memory_label.grid(row=0, column=0, sticky=W)
        boldseperator.grid(row=0, column=1, sticky=S)
        self.pc_frame.grid(row=0, column=2, sticky=NS)
        self.pc_label.grid(row=0, column=3, sticky=NS)
        seperator1.grid(row=0, column=4, sticky=NS)
        self.acc_frame.grid(row=0, column=5, sticky=NS)
        self.acc_label.grid(row=0, column=6, sticky=NS)
        seperator2.grid(row=0, column=7, sticky=NS)
        self.status_label.grid(row=0, column=8, sticky=NSEW)
        boldseperator1.grid(row=1, column=0, columnspan=9, sticky=EW)

        # Update memory text to expand
        self.memory_text.grid(row=2, column=0, columnspan=9, sticky="nsew")  # Ensure it fills the space

        # Initialize memory display with initial memory data and disable input
        self.memory_text.config(state=tk.NORMAL)
        self.update_memory_text(self.mem.__str__())
        self.memory_text.tag_add("center", "1.0", "end")  # Center the rest of the text
        self.memory_text.config(state=tk.DISABLED)
        self.memory_text.bind("<Configure>", self.adjust_memory_font_size) # Binds the adjust memory font size when window is changed

        return memory_frame

    def setup_control_frame(self, main_frame):
        '''Sets up the control frame for controlling the program.
        Args:
            main_frame (ttk.Frame): The parent frame to place the control frame in.
        Returns:
            ttk.Frame: The created control frame containing program control buttons and I/O.
        '''
        # Declare and Place run, step, halt, reset buttons, and I/O text in Control Frame
        control_frame = ttk.Frame(main_frame, style='Primary.TFrame', padding=10)
        control_frame.grid_columnconfigure(2, weight=1)  # Allow the I/O to expand horizontally

        run_btn = ttk.Button(control_frame, text="Run", command=self.run_program, padding=5)
        step_btn = ttk.Button(control_frame, text="Step", command=self.step_program, padding=5)
        halt_btn = ttk.Button(control_frame, text="Halt", command=self.halt_program, padding=5)
        reset_btn = ttk.Button(control_frame, text="Reset", command=self.reset_program, padding=5)
        seperator3 = ttk.Separator(control_frame, orient=VERTICAL)
        self.io_label = tk.Label(control_frame, text="I/O", font=FONT["secondary"],
                              bg=self.secondary_color, fg=self.secondary_text_color, padx=5)
        self.io_text = ttk.Entry(control_frame, font=FONT["primary"], state=tk.DISABLED, style='IO.TEntry')

        control_frame.grid(row=2, column=0, sticky="sew")  # Stick to bottom

        run_btn.grid(row=0, rowspan=2, column=0, padx=5, pady=5, sticky="w")
        step_btn.grid(row=0, rowspan=2, column=1, padx=5, pady=5, sticky="w")
        halt_btn.grid(row=2, rowspan=2, column=0, padx=5, pady=5, sticky="w")
        reset_btn.grid(row=2, rowspan=2, column=1, padx=5, pady=5, sticky="w")
        seperator3.grid(row=0, rowspan=4, column=2, sticky="nsw")
        self.io_label.grid(row=0, column=2, padx=5, pady=(5, 0), sticky="nsw")
        self.io_text.grid(row=1, rowspan=3, column=2, padx=5, pady=5, sticky="sew")

        return control_frame

    def save_file(self, file_path=None):
        '''Save the contents of the program_text widget to a file'''
        if not file_path:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        try:
            with open(file_path, "w") as file:
                file.write(self.program_text.get("1.0", tk.END))
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
            return
        self.status_label.config(text="Status: File saved successfully")


    def load_file(self, file_path=None):
        '''Load a file into the program_text widget'''
        if not file_path:
            file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        self.program_text.delete("1.0", tk.END)
        
        try:
            with open(file_path, "r") as file:
                text = file.read()

                lines = text.split("\n")
                data = ""

                for index, line in enumerate(lines):
                    data += line.split()[0]  
                    if index != len(lines)-1:
                        data += "\n"                
                
                self.program_text.insert(tk.END, data)

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
        # Execute if program_text widget is not empty
        if (self.program_text.get("1.0", tk.END).strip()):
            text = self.program_text.get("1.0", tk.END).splitlines()
            self.mem.clear()

            try:
                self.boot.load_program(text)                

            except IndexError as e:
                messagebox.showerror("Error", f"Invalid address: {str(e)}")
                return
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid instruction: {str(e)}")
                return
            self.status_label.config(text="Status: Ready")
            self.update_memory_text()
            # Switch focus to memory frame after loading
            self.highlight_main_frame()

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

        # Update the colors for the memory text widget
        self.memory_text.set_colors(self.primary_text_color, self.pc_text_color)

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
                if i * len(instructions) + j - i == pc + 1:
                    self.memory_text.insert_colored_text(instruction + " ", "secondary")
                    # Display the current instruction in the instructions label
                    try:
                        self.instructions.config(text=f"{self.cpu.operation(self.mem.word_to_int(instruction), self, True)}")
                    except:
                        self.instructions.config(text="Instruction")
                else:
                    self.memory_text.insert_colored_text(instruction + " ", "primary")
            if not line[0:2] == "90": # Don't add a newline if it is the last line
                self.memory_text.insert_colored_text("\n")
            
        self.memory_text.tag_add("center", "1.0", "end")
        self.memory_text.config(state=tk.DISABLED)
        self.pc_label.config(text=f"{self.cpu.pointer:02d}") # Ensure PC is always 2 digits
        self.acc_label.config(text=f"{"+" if self.cpu.accumulator >= 0 else "-"}{abs(int(self.cpu.accumulator)):04d}") # Ensure accumulator is always at least 5 digits
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
        # Switch focus to main frame when running
        self.highlight_main_frame()
            
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

        try:
            operand = self.mem.word_to_int(self.mem.read(self.cpu.pointer))
            self.cpu.pointer += 1
            self.cpu.operation(operand, self)
        
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

        # Highlight the program frame
        self.highlight_program_frame()

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

    def open_color_dialog(self):
        '''Open the color chooser dialog'''
        color_dialog = ColorChooser(self)  # Pass the App instance directly
        color_dialog.show()
        
        # Update color indicator button after dialog closes
        if hasattr(self, 'color_indicator'):
            self.color_indicator.configure(bg=self.primary_color)

    def setup_styles(self):
        '''Set up ttk styles and custom widget appearances'''
        self.style = ttk.Style(self.root)
        self.style.theme_use("alt")
        
        # Define frame styles
        self.style.configure('Primary.TFrame', background=self.primary_color)
        self.style.configure('Secondary.TFrame', background=self.secondary_color)
        self.style.configure('Darkened.TFrame', background=self.darken_color(self.primary_color))
        
        # Define button style
        self.style.configure('TButton', 
                            background=self.secondary_color,
                            foreground=self.secondary_text_color)
        
        # Define entry style
        self.style.configure('IO.TEntry', 
                            fieldbackground=self.secondary_color,
                            foreground=self.secondary_text_color,
                            background=self.secondary_color)
        
        # Define disabled entry style
        self.style.map('IO.TEntry',
                      fieldbackground=[('disabled', self.secondary_color)],
                      foreground=[('disabled', self.primary_text_color)],
                      background=[('disabled', self.primary_color)])

    def apply_colors(self):
        '''Apply current color settings to all UI elements by updating styles'''
        # Update all styles with current colors
        self.style.configure('Primary.TFrame', background=self.primary_color)
        self.style.configure('Secondary.TFrame', background=self.secondary_color)
        self.style.configure('Darkened.TFrame', background=self.darken_color(self.primary_color))
        
        # Only keep the ttk styles we're using
        self.style.configure('TButton', 
                            background=self.secondary_color,
                            foreground=self.secondary_text_color)
        
        self.style.configure('IO.TEntry', 
                            fieldbackground=self.secondary_color,
                            foreground=self.secondary_text_color)
        
        # Update disabled state colors
        self.style.map('IO.TEntry',
                      fieldbackground=[('disabled', self.secondary_color)],
                      foreground=[('disabled', self.primary_text_color)],
                      background=[('disabled', self.primary_color)])
        
        # Root background (not a ttk widget)
        self.root.configure(bg=self.primary_color)
        
        # Regular Text widgets (not ttk)
        self.program_text.configure(
            bg=self.secondary_color,
            fg=self.primary_text_color,
        )
        
        self.memory_text.configure(
            bg=self.secondary_color,
            fg=self.primary_text_color
        )
        
        # Update all labels manually as ttk labels won't work on mac, and I am not sure why
        if hasattr(self, 'instructions'):
            self.instructions.configure(bg=self.secondary_color, fg=self.primary_text_color)
            
        if hasattr(self, 'memory_label'):
            self.memory_label.configure(bg=self.secondary_color, fg=self.primary_text_color)
            
        if hasattr(self, 'pc_label'):
            self.pc_label.configure(bg=self.secondary_color, fg=self.primary_text_color)
            
        if hasattr(self, 'acc_label'):
            self.acc_label.configure(bg=self.secondary_color, fg=self.primary_text_color)
            
        if hasattr(self, 'pc_frame'):
            self.pc_frame.configure(bg=self.secondary_color, fg=self.primary_text_color)
            
        if hasattr(self, 'acc_frame'):
            self.acc_frame.configure(bg=self.secondary_color, fg=self.primary_text_color)
            
        if hasattr(self, 'status_label'):
            self.status_label.configure(bg=self.secondary_color, fg=self.primary_text_color)
            
        if hasattr(self, 'io_label'):
            self.io_label.configure(bg=self.secondary_color, fg=self.primary_text_color)
        
        # Update color indicator button if it exists
        if hasattr(self, 'color_indicator'):
            self.color_indicator.configure(bg=self.primary_color)
        
        self.update_memory_text()
        # Refresh UI
        self.root.update_idletasks()

    def highlight_program_frame(self):
        '''Highlight the program frame and darken other frames'''
        self.program_frame.configure(style='Primary.TFrame')
        self.instruction_frame.configure(style='Darkened.TFrame')
        self.memory_frame.configure(style='Darkened.TFrame')
        self.control_frame.configure(style='Darkened.TFrame')

        self.update_memory_text()

    def highlight_main_frame(self):
        '''Highlight the memory frame and darken other frames'''
        self.program_frame.configure(style='Darkened.TFrame')
        self.instruction_frame.configure(style='Primary.TFrame')
        self.memory_frame.configure(style='Primary.TFrame')
        self.control_frame.configure(style='Primary.TFrame')

        self.update_memory_text()

    def darken_color(self, color, factor=0.4):
        '''Darken a hex color by a given factor'''
        # Remove the '#' if present
        color = color.lstrip('#')
        
        # Convert hex to RGB
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Darken each component
        darkened_rgb = tuple(int(c * factor) for c in rgb)
        
        # Convert back to hex
        return '#{:02x}{:02x}{:02x}'.format(*darkened_rgb)
