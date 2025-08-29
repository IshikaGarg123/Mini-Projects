# Import necessary libraries
import tkinter as tk  # For GUI elements
from tkinter import ttk, messagebox  # For combobox and popup messages
from PIL import Image, ImageTk  # For loading and displaying flag images
import os  # For file path handling

# Static exchange rates (used for conversion)
exchange_rates = {
    'INR': 1.0,
    'USD': 0.012,
    'EUR': 0.011,
    'GBP': 0.0095,
    'JPY': 1.78,
    'CAD': 0.016
}

# Currency full names (for better readability in dropdowns)
currency_names = {
    'INR': 'Indian Rupee',
    'USD': 'US Dollar',
    'EUR': 'Euro',
    'GBP': 'British Pound',
    'JPY': 'Japanese Yen',
    'CAD': 'Canadian Dollar'
}

# Main class for the Currency Converter Application
class CurrencyConverterApp:
    def __init__(self, root):
        # Set window properties
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("600x550")
        self.root.config(bg="#E8F0FE")  # Light background color

        self.flags = {}  # Dictionary to store loaded flag images

        # Application Title
        tk.Label(root, text="💱 Currency Converter", font=("Segoe UI", 22, "bold"),
                 bg="#E8F0FE", fg="#333").pack(pady=10)

        # Frame for entering amount
        entry_frame = tk.Frame(root, bg="#E8F0FE")
        entry_frame.pack()

        # Label and entry for amount
        tk.Label(entry_frame, text="Enter Amount:", bg="#E8F0FE", font=("Segoe UI", 12)).grid(row=0, column=0, pady=5)
        self.amount_entry = tk.Entry(entry_frame, font=("Segoe UI", 14), width=20,
                                     justify="center", bd=2, relief="groove")
        self.amount_entry.grid(row=1, column=0, padx=10)

        # Frame for currency selection and swap button
        currency_frame = tk.Frame(root, bg="#E8F0FE")
        currency_frame.pack(pady=10)

        # FROM currency flag image (Label)
        self.from_flag = tk.Label(currency_frame, bg="#E8F0FE")
        self.from_flag.grid(row=0, column=0, padx=5)

        # FROM currency dropdown
        self.from_currency = ttk.Combobox(currency_frame, font=("Segoe UI", 12),
                                          state="readonly", width=25)
        self.from_currency.grid(row=0, column=1, padx=5)

        # Swap button between currencies
        swap_btn = tk.Button(currency_frame, text="⇄", font=("Arial", 14, "bold"),
                             command=self.swap_currencies, bg="#4CAF50",
                             fg="white", width=3)
        swap_btn.grid(row=0, column=2)

        # TO currency flag image (Label)
        self.to_flag = tk.Label(currency_frame, bg="#E8F0FE")
        self.to_flag.grid(row=0, column=3, padx=5)

        # TO currency dropdown
        self.to_currency = ttk.Combobox(currency_frame, font=("Segoe UI", 12),
                                        state="readonly", width=25)
        self.to_currency.grid(row=0, column=4, padx=5)

        # Frame for Convert button
        button_frame = tk.Frame(root, bg="#E8F0FE")
        button_frame.pack(pady=10)

        # Convert button to perform currency conversion
        convert_btn = tk.Button(button_frame, text="Convert", command=self.convert_currency,
                                font=("Segoe UI", 12, "bold"), bg="#007ACC",
                                fg="white", padx=15, pady=5)
        convert_btn.pack()

        # Label to display the result of conversion
        self.result_label = tk.Label(root, text="", font=("Segoe UI", 16, "bold"),
                                     bg="#E8F0FE", fg="#000")
        self.result_label.pack(pady=10)

        # Label above the history list
        tk.Label(root, text="🕓 Conversion History", font=("Segoe UI", 12, "bold"),
                 bg="#E8F0FE").pack()

        # Listbox to display conversion history
        self.history_box = tk.Listbox(root, height=7, width=70, font=("Courier New", 10))
        self.history_box.pack(pady=5)

        # Load dropdown values and flag images
        self.load_currency_dropdowns()

        # Bind flag updates on dropdown selection
        self.from_currency.bind("<<ComboboxSelected>>", self.update_flags)
        self.to_currency.bind("<<ComboboxSelected>>", self.update_flags)

        # Set default selections
        self.from_currency.set("INR - Indian Rupee")
        self.to_currency.set("USD - US Dollar")
        self.update_flags()  # Show initial flags

    # Method to load currencies into dropdowns and flags
    def load_currency_dropdowns(self):
        items = []  # List for combobox items
        for code in exchange_rates:
            name = currency_names[code]
            items.append(f"{code} - {name}")

            # Load and resize flag image from file
            img_path = os.path.join("flags", f"{code}.png")
            if os.path.exists(img_path):
                image = Image.open(img_path).resize((32, 20))
                self.flags[code] = ImageTk.PhotoImage(image)

        # Set dropdown options
        self.from_currency["values"] = items
        self.to_currency["values"] = items

    # Update flag images based on selected currencies
    def update_flags(self, event=None):
        from_code = self.from_currency.get().split(" - ")[0]
        to_code = self.to_currency.get().split(" - ")[0]

        # Update flag images beside combobox
        self.from_flag.config(image=self.flags.get(from_code))
        self.to_flag.config(image=self.flags.get(to_code))

    # Main function to perform currency conversion
    def convert_currency(self):
        try:
            # Get amount from input field
            amount = float(self.amount_entry.get())

            # Extract selected currency codes
            from_code = self.from_currency.get().split(" - ")[0]
            to_code = self.to_currency.get().split(" - ")[0]

            # Error if both currencies are the same
            if from_code == to_code:
                messagebox.showwarning("Invalid Selection", "Please select different currencies.")
                return

            # Calculate converted amount
            result = amount * (exchange_rates[to_code] / exchange_rates[from_code])

            # Display result
            self.result_label.config(text=f"{amount:.2f} {from_code} = {result:.2f} {to_code}")

            # Add to conversion history
            self.history_box.insert(tk.END, f"{amount:.2f} {from_code} → {result:.2f} {to_code}")

        except ValueError:
            # Handle non-numeric input
            messagebox.showerror("Invalid Input", "Please enter a valid numeric amount.")

    # Function to swap selected currencies
    def swap_currencies(self):
        # Get current selections
        from_val = self.from_currency.get()
        to_val = self.to_currency.get()

        # Swap values in dropdowns
        self.from_currency.set(to_val)
        self.to_currency.set(from_val)

        # Update flag display
        self.update_flags()


# Create main window and run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
