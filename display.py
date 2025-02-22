import obd
import time
import tkinter as tk
from tkinter import messagebox

# Initialize OBD2 connection (use the correct COM port)
connection = obd.OBD(portname="COM3")  # Replace with your actual COM port

# Define shift point (3000 RPM)
shift_point = 3000

# Function to show the visual alert
def show_shift_alert():
    # Create the main window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Show a message box with a shift alert
    messagebox.showwarning("Shift Alert", "Time to shift gears!")

    # Close the alert window after it's acknowledged
    root.destroy()

while True:
    # Get current RPM
    rpm = connection.query(obd.commands.RPM)

    if rpm.is_null():
        print("Unable to read RPM")
    else:
        current_rpm = rpm.value
        print(f"Current RPM: {current_rpm}")

        # Check if it's time to shift
        if current_rpm >= shift_point:
            show_shift_alert()  # Trigger the visual alert
            
    time.sleep(0.5)  # Delay for half a second before next check
