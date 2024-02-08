import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from HopperSpecification import *                                                                                       #This is a constructor where several conical hoppers are defined as objects
from vessel_volume import *                                                                                             #This function estimates the volume of the hoppers
from height_position import *                                                                                           #This function estimates the height ("HEIGHT") of the powder in the hopper. It also gives the radius (RADIUS) corresponds to the height of the powder in the hopper
import matplotlib.pyplot as plt

# Declare plot_frame as a global variable
plot_frame = None

def validate_input():
    try:
        mass = float(mass_var.get())
        density = float(density_var.get())

        if mass < 0 or density < 0:
            messagebox.showerror("Error", "Mass and density must be non-negative numbers.")
            return False

        return True
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for mass and density.")
        return False

def calculate():
    # Validate input
    if not validate_input():
        return

    # Extract the numerical value associated with the selected equipment
    selected_equipment = equipment_var.get()
    equipment_number = next(item[1] for item in equipment_options if item[0] == selected_equipment)

    k = equipment_number    # storing the euqipment ID in k
    X = r[k - 1].x  # X values for the position of the vessel
    Z = r[k - 1].z  # Z values (height) for the position of the vessel
    # This function estimates the volume of the vessel (m3)
    # percent is the volume percent associated with each section of the hopper
    [volume, percent, vol] = vessel_volume(X, Z)

    fill_percent = 100 * (float(mass_var.get()) / (float(density_var.get()) * 1000)) / (volume)
    if fill_percent > 100:
        print("The volume of the material exceeds the volume of the hopper! I have to stop the code!")
        messagebox.showerror("Error", "The volume of the material exceeds the volume of the hopper! I have to stop the code!")
        return False

    # This function estimates the HEIGHT of the material in the hopper (m)
    # It also gives the radius (or x-location) associated with the height of the powder
    [HEIGHT, RADIUS] = height_position(X, Z, fill_percent)

    # This function estimates the HEIGHT of the material in the hopper (m)
    # It also gives the radius (or x-location) associated with the height of the powder

    # Your specific calculation logic here
    result1 = HEIGHT
    result2 = fill_percent
    result3 = volume * 1000         # change it into liter
    # Update the result_label
    result_text1 = f"Filling height is: {round(result1,2)} m "
    result_text2 = f"Filling percent is: {round(result2,2)} "
    result_text3 = f"Volume of the equipment is: {round(result3, 2)} liter "

    result1_label.config(text=[result_text1])
    result2_label.config(text=[result_text2])
    result3_label.config(text=[result_text3])

    ## showing the dimensions of the hopper
    percent = percent[::-1]  # reversing the percent of filling order for convinience
    plt.plot(r[k - 1].x, r[k - 1].z, 'b-')
    plt.plot([-x for x in r[k - 1].x], r[k - 1].z, 'b-')
    ## putting label of percent of filling
    for i in range(len(X) - 1):
        plt.text(X[i], Z[i], 'filling%: {}'.format(round(percent[i], 1)), fontsize=16, color='g')
        plt.axhline(Z[i], color='g', linestyle='--')
    plt.axhline(HEIGHT, color='r', linestyle='--')
    plt.xlabel("x-axis (m)", fontsize=16)
    plt.ylabel("y-axis (m)", fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    volume_liter = round(1000 * volume, 2)  # m3 to liter
    plt.title("The volume of %s" % r[k - 1].name + f" is {volume_liter:0.2f} liter." +"\n The filling percent is %0.1f" %fill_percent, fontsize=14)
    plt.show()

    # Plot the result
    #plot_result(r[k - 1].x, [r[k - 1].z])

def plot_result(result):
    # Clear previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Create a new figure for the plot
    fig = Figure(figsize=(5, 4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    plot.bar(["Result"], [result])

    # Embed the plot in the Tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create the main application window
app = tk.Tk()
app.title("Equipment Calculator")

# Create and place input widgets (Entry for mass and density, Dropdown for equipment selection)
mass_label = ttk.Label(app, text="Enter the mass of material (kg) ")
mass_label.grid(row=0, column=0, padx=10, pady=10)
mass_var = tk.StringVar()
mass_entry = ttk.Entry(app, textvariable=mass_var)
mass_entry.grid(row=0, column=1, padx=10, pady=10)

density_label = ttk.Label(app, text="Enter the average consolidated bulk density of the material (gram/ml) ")
density_label.grid(row=1, column=0, padx=10, pady=10)
density_var = tk.StringVar()
density_entry = ttk.Entry(app, textvariable=density_var)
density_entry.grid(row=1, column=1, padx=10, pady=10)

equipment_label = ttk.Label(app, text="Equipment:")
equipment_label.grid(row=2, column=0, padx=10, pady=10)
equipment_options = [
    ("1000L_IBC", 1),
    ("100L_IBC", 2),
    ("Piccola", 3),
    ("Courtoy", 4),
    ("Kosrsch_XL100_poor_flow", 5),
    ("Korsch_XL100_gravity", 6),
    ("300L_IBC", 7),
]

equipment_var = tk.StringVar()
equipment_dropdown = ttk.Combobox(app, textvariable=equipment_var, values=[item[0] for item in equipment_options])
equipment_dropdown.grid(row=2, column=1, padx=10, pady=10)

# Create and place a button to trigger the calculation
calculate_button = ttk.Button(app, text="Calculate", command=calculate)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

# Create a label to display the result
result1_label = ttk.Label(app, text="Filling height: ")
result1_label.grid(row=4, column=0, columnspan=2, pady=10)
result2_label = ttk.Label(app, text="Filling percent: ")
result2_label.grid(row=5, column=0, columnspan=2, pady=10)
result3_label = ttk.Label(app, text="Volume of the equipment: ")
result3_label.grid(row=6, column=0, columnspan=2, pady=10)

# Create a frame to hold the plot
plot_frame = ttk.Frame(app)
plot_frame.grid(row=5, column=0, columnspan=2, pady=10)

# Start the GUI application
app.mainloop()
