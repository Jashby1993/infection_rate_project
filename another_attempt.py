import tkinter as tk
from tkinter import messagebox

def submit(disease_entry, population_entry, starting_infected_entry, infection_rate_entry, mortality_rate_entry):
    disease_info = {}
    disease_info['disease_name'] = disease_entry.get()
    disease_info['total_population'] = population_entry.get()
    disease_info['starting_infected'] = starting_infected_entry.get()
    disease_info['infection_rate'] = infection_rate_entry.get()
    disease_info['mortality_rate'] = mortality_rate_entry.get()

    # Validate the input values
    try:
        total_population = int(disease_info['total_population'])
        if not (100 <= total_population <= 800):
            raise ValueError("Total population must be between 100 and 800")
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
        return

    try:
        starting_infected = int(disease_info['starting_infected'])
        if not (1 <= starting_infected <= 20):
            raise ValueError("Starting infected must be between 1 and 20")
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
        return

    try:
        infection_rate = float(disease_info['infection_rate'])
        if not (0.50 <= infection_rate <= 0.9969):
            raise ValueError("Infection rate must be a float between 0.50 and 0.9969")
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
        return

    try:
        mortality_rate = float(disease_info['mortality_rate'])
        if not (0.00 <= mortality_rate <= 0.25):
            raise ValueError("Mortality rate must be a float between 0.00 and 0.25")
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
        return

    # Return the dictionary
    return disease_info

def create_gui(root):
    disease_label = tk.Label(root, text="Disease Name:")
    disease_label.grid(row=0, column=0, padx=5, pady=5)
    disease_entry = tk.Entry(root)
    disease_entry.grid(row=0, column=1, padx=5, pady=5)

    # Create labels and entry fields for other disease information...
    
    submit_button = tk.Button(root, text="Start Simulation", command=lambda: submit(disease_entry, population_entry, starting_infected_entry, infection_rate_entry, mortality_rate_entry))
    submit_button.grid(row=10, column=0, columnspan=2, padx=5, pady=10)

    # Create and place other entry fields and labels...
    population_label = tk.Label(root, text="Total Population:")
    population_label.grid(row=2, column=0, padx=5, pady=5)
    population_entry = tk.Entry(root)
    population_entry.grid(row=2, column=1, padx=5, pady=5)
    population_info = tk.Label(root, text="(Must be an integer between 100 and 800)", fg="gray")
    population_info.grid(row=3, column=1, padx=5, sticky='w')

    starting_infected_label = tk.Label(root, text="Starting Infected:")
    starting_infected_label.grid(row=4, column=0, padx=5, pady=5)
    starting_infected_entry = tk.Entry(root)  # Entry field for starting infected
    starting_infected_entry.grid(row=4, column=1, padx=5, pady=5)
    starting_infected_info = tk.Label(root, text="(Must be an integer between 1 and 20)", fg="gray")
    starting_infected_info.grid(row=5, column=1, padx=5, sticky='w')

    infection_rate_label = tk.Label(root, text="Infection Rate:")
    infection_rate_label.grid(row=6, column=0, padx=5, pady=5)
    infection_rate_entry = tk.Entry(root)
    infection_rate_entry.grid(row=6, column=1, padx=5, pady=5)
    infection_rate_info = tk.Label(root, text="(Must be a decimal between 0.50 and 0.9969)", fg="gray")
    infection_rate_info.grid(row=7, column=1, padx=5, sticky='w')

    mortality_rate_label = tk.Label(root, text="Mortality Rate:")
    mortality_rate_label.grid(row=8, column=0, padx=5, pady=5)
    mortality_rate_entry = tk.Entry(root)
    mortality_rate_entry.grid(row=8, column=1, padx=5, pady=5)
    mortality_rate_info = tk.Label(root, text="(Must be a float between 0.00 and 0.25)", fg="gray")
    mortality_rate_info.grid(row=9, column=1, padx=5, sticky='w')

    # Return entry fields
    return disease_entry, population_entry, starting_infected_entry, infection_rate_entry, mortality_rate_entry

def main():
    root = tk.Tk()
    root.title("Disease Information")
    disease_entry, population_entry, starting_infected_entry, infection_rate_entry, mortality_rate_entry = create_gui(root)
    root.mainloop()

    # This part is moved after the mainloop so that the user has a chance to input data
    user_info = submit(disease_entry, population_entry, starting_infected_entry, infection_rate_entry, mortality_rate_entry)
    print(user_info)

if __name__ == "__main__":
    main()

