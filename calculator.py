import tkinter as tk  # Import tkinter for GUI
from ttkbootstrap import Style  # Import ttkbootstrap for modern themes
from ttkbootstrap.widgets import Entry, Button, Frame, Label  # Import specific ttkbootstrap widgets
import math  # Import math module for scientific calculations
# === Setup ===
        
style = Style("flatly")  # Set the theme for the calculator ("superhero" for dark mode)
style.configure("Digit.TButton", font=("Helvetica", 12, "bold"))  # Style for digit buttons
style.configure("Operator.TButton", font=("Helvetica", 11))  # Style for operator buttons

root = style.master  # Get the root window from the style
root.title("Advanced Calculator")  # Set the window title
root.geometry("420x650")  # Set the size of the window
root.resizable(True, True)  # Make the window resizable


# === Expression Handling ===
expression = ""  # Global variable to store user input

def update_display(value):  # Function to update display with user input
    global expression
    expression += str(value)  # Add character to expression
    display.delete(0, tk.END)  # Clear previous display
    display.insert(tk.END, expression)  # Show updated expression

def clear_display():  # Function to clear display
    global expression
    expression = ""
    display.delete(0, tk.END)

def backspace():  # Function to remove last character
    global expression
    expression = expression[:-1]
    display.delete(0, tk.END)
    display.insert(tk.END, expression)

def calculate():  # Function to evaluate expression
    global expression
    try:
        # Replace operators and functions with math equivalents
        result = str(eval(expression.replace('√', 'math.sqrt')
                          .replace('π', 'math.pi')
                          .replace('e', 'math.e')
                          .replace('sin', 'math.sin')
                          .replace('cos', 'math.cos')
                          .replace('tan', 'math.tan')
                          .replace('log', 'math.log10')
                          .replace('ln', 'math.log')
                          .replace('^', '**')
                          .replace('÷', '/')
                          .replace('×', '*')))
        add_to_history(expression + " = " + result)  # Add to history panel
        expression = result  # Store result for next operation
        display.delete(0, tk.END)
        display.insert(tk.END, result)
    except:
        display.delete(0, tk.END)
        display.insert(tk.END, "Error")
        expression = ""

# === Display ===
display = Entry(root, font=("Helvetica", 20), justify="right")  # Input display field
display.pack(fill='x', padx=10, pady=10, ipady=10)  # Pack display with padding

# === Button Frames ===
button_frame = Frame(root)  # Frame for main calculator buttons
button_frame.pack(fill='both', expand=True)

sci_frame = Frame(root)  # Frame for scientific buttons
sci_frame.pack(fill='x', padx=10)

# === History Panel ===
def add_to_history(entry):  # Function to add calculation history
    history_text.config(state='normal')
    history_text.insert(tk.END, entry + "\n")
    history_text.see(tk.END)
    history_text.config(state='disabled')

history_label = Label(root, text="History", font=("Helvetica", 12, "bold"))  # Label for history
history_label.pack()
history_text = tk.Text(root, height=4, font=("Courier", 10), state='disabled')  # Text area for history
history_text.pack(fill='both', padx=10, pady=(0, 10))

# === Scientific Buttons ===
sci_buttons = ['sin(', 'cos(', 'tan(', 'log(', 'ln(', '√(', 'π', 'e', '^']  # List of scientific operators
for i, text in enumerate(sci_buttons):
    sci_btn = Button(sci_frame, text=text, width=6, bootstyle="warning", command=lambda x=text: update_display(x))  # Create button
    sci_btn.grid(row=0, column=i, padx=2, pady=4)  # Place in grid

# === Main Calculator Buttons ===
buttons = [
    ['C', '←', '(', ')'],
    ['7', '8', '9', '÷'],
    ['4', '5', '6', '×'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
]  # Layout for main calculator

for i, row in enumerate(buttons):  # Loop through rows
    for j, text in enumerate(row):  # Loop through each button
        # Decide button style based on type
        if text.isdigit():  # If it's a digit
            btn_style = "dark"
            btn_ttkstyle = "Digit.TButton"
        else:
            btn_style = "secondary"
            btn_ttkstyle = "Operator.TButton"

        # Assign appropriate action
        action = lambda x=text: (
            clear_display() if x == 'C' else
            backspace() if x == '←' else
            calculate() if x == '=' else
            update_display(x)
        )

        # Create the button
        btn = Button(button_frame, text=text, width=6, bootstyle=btn_style,
                     command=action, style=btn_ttkstyle)
        btn.grid(row=i, column=j, padx=5, pady=5, ipadx=4, ipady=10, sticky='nsew')  # Place button

        # Hover effects
        btn.bind("<Enter>", lambda e, b=btn: b.configure(bootstyle="success"))  # On hover
        btn.bind("<Leave>", lambda e, b=btn, s=btn_style: b.configure(bootstyle=s))  # On leave

# === Resize Support ===
for i in range(5):
    button_frame.rowconfigure(i, weight=1)  # Make rows expandable
for j in range(4):
    button_frame.columnconfigure(j, weight=1)  # Make columns expandable

# === Keyboard Bindings ===
def key_handler(event):  # Handle keyboard input
    key = event.char
    if key in '0123456789.+-*/()':  # Add character
        update_display(key)
    elif key == '\r':  # Enter key = calculate
        calculate()
    elif key == '\x08':  # Backspace
        backspace()
    elif key == '\x1b':  # Escape clears display
        clear_display()

root.bind("<Key>", key_handler)  # Bind key events to handler

# === Start App ===
root.mainloop()  # Start the GUI loop
