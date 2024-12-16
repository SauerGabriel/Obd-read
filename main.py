import obd
import tkinter as tk
from tkinter import messagebox

# Connect to the OBD-II adapter
connection = obd.OBD(/dev/rfcomm2)  # Leave () blank to auto detect or specify the port

# Check if the connection is successful
if not connection.is_connected():
    print("Unable to connect to OBD-II adapter.")
    exit()

# Supported commands
RPM_COMMAND = obd.commands.RPM
SPEED_COMMAND = obd.commands.SPEED
BOOST_PRESSURE_COMMAND = obd.commands.BOOST

# Function to calculate gear based on RPM and speed
def get_gear(rpm, speed):
    if speed == 0 or rpm == 0:
        return "N"  # Neutral or stopped
    gear_ratios = [3.583, 1.947, 1.379, 1.030, 0.820]  # Example gear ratios
    final_drive = 4.312  # Final drive ratio for Lancer Ralliart
    tire_diameter = 0.634  # Example in meters (adjust for your tires)
    wheel_circumference = tire_diameter * 3.1416
    speed_mps = speed / 3.6  # Convert km/h to m/s

    for i, ratio in enumerate(gear_ratios):
        theoretical_speed = (rpm / (ratio * final_drive)) * wheel_circumference * 60 / 1000
        if abs(theoretical_speed - speed_mps) < 3:  # Match threshold
            return i + 1  # Gear number starts at 1
    return "N/A"

# Function to read OBD data
def update_obd_data():
    global warning_rpm

    # Read RPM
    rpm_response = connection.query(RPM_COMMAND)
    rpm = rpm_response.value.magnitude if rpm_response.value else 0

    # Read speed
    speed_response = connection.query(SPEED_COMMAND)
    speed = speed_response.value.magnitude if speed_response.value else 0

    # Read turbo pressure (if supported)
    boost_response = connection.query(BOOST_PRESSURE_COMMAND)
    turbo_pressure = boost_response.value.magnitude if boost_response.value else 0

    # Determine gear
    gear = get_gear(rpm, speed)

    # Update GUI labels
    rpm_label.config(text=f"RPM: {rpm}")
    gear_label.config(text=f"Gear: {gear}")
    turbo_label.config(text=f"Turbo Pressure: {turbo_pressure} kPa")

    # Check for gear change warning
    if rpm >= warning_rpm:
        messagebox.showwarning("Gear Change Alert", f"Consider changing gear. RPM is {rpm}!")

    # Schedule next update
    root.after(1000, update_obd_data)  # Update every 1 second

# Function to set the warning RPM
def set_warning_rpm():
    global warning_rpm
    try:
        warning_rpm = int(rpm_entry.get())
        rpm_warning_label.config(text=f"Warning RPM: {warning_rpm}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid integer for RPM.")

# Initialize global warning RPM
warning_rpm = 4000

# Create GUI
root = tk.Tk()
root.title("Car Information - OBD-II")

# RPM label
rpm_label = tk.Label(root, text="RPM: N/A", font=("Arial", 16))
rpm_label.pack()

# Gear label
gear_label = tk.Label(root, text="Gear: N/A", font=("Arial", 16))
gear_label.pack()

# Turbo pressure label
turbo_label = tk.Label(root, text="Turbo Pressure: N/A", font=("Arial", 16))
turbo_label.pack()

# Warning RPM input
rpm_input_frame = tk.Frame(root)
rpm_input_frame.pack(pady=10)

rpm_entry_label = tk.Label(rpm_input_frame, text="Set Warning RPM: ")
rpm_entry_label.pack(side=tk.LEFT)

rpm_entry = tk.Entry(rpm_input_frame)
rpm_entry.pack(side=tk.LEFT)

set_rpm_button = tk.Button(rpm_input_frame, text="Set", command=set_warning_rpm)
set_rpm_button.pack(side=tk.LEFT)

# Current warning RPM label
rpm_warning_label = tk.Label(root, text=f"Warning RPM: {warning_rpm}", font=("Arial", 12))
rpm_warning_label.pack()

# Start updating OBD data
update_obd_data()

# Run the GUI event loop
root.mainloop()
