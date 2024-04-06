import tkinter as tk
from tkinter import messagebox

def submit():
    # Retrieve values entered by the user
    disease_name = disease_entry.get()
    total_population = population_entry.get()
    infection_rate = infection_rate_entry.get()
    mortality_rate = mortality_rate_entry.get()

    # Validate the input values
    if not (100 <= int(total_population) <= 800):
        messagebox.showerror("Error", "Total population must be between 100 and 800")
        return
    try:
        infection_rate = float(infection_rate)
        if not (0.50 <= infection_rate <= 0.9969):
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Infection rate must be a float between 0.50 and 0.9969")
        return

    try:
        mortality_rate = float(mortality_rate)
        if not (0.00 <= mortality_rate <= 0.25):
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Mortality rate must be a float between 0.00 and 0.25")
        return

    # Print the entered values
    print("Disease Name:", disease_name)
    print("Total Population:", total_population)
    print("Infection Rate:", infection_rate)
    print("Mortality Rate:", mortality_rate)

# Create the main window
root = tk.Tk()
root.title("Disease Information")

# Create labels and entry fields for disease information
disease_label = tk.Label(root, text="Disease Name:")
disease_label.grid(row=0, column=0, padx=5, pady=5)
disease_entry = tk.Entry(root)
disease_entry.grid(row=0, column=1, padx=5, pady=5)

population_label = tk.Label(root, text="Total Population:")
population_label.grid(row=1, column=0, padx=5, pady=5)
population_entry = tk.Entry(root)
population_entry.grid(row=1, column=1, padx=5, pady=5)

infection_rate_label = tk.Label(root, text="Infection Rate:")
infection_rate_label.grid(row=2, column=0, padx=5, pady=5)
infection_rate_entry = tk.Entry(root)
infection_rate_entry.grid(row=2, column=1, padx=5, pady=5)

mortality_rate_label = tk.Label(root, text="Mortality Rate:")
mortality_rate_label.grid(row=3, column=0, padx=5, pady=5)
mortality_rate_entry = tk.Entry(root)
mortality_rate_entry.grid(row=3, column=1, padx=5, pady=5)

# Create a button to submit the input
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

# Run the application
root.mainloop()