import obd
import time
import tkinter as tk
from tkinter import messagebox

# Initialize OBD2 connection (use the correct COM port)
connection = obd.OBD(portname="COM3")  # Replace with your actual COM port

# Define shift point (3000 RPM)
shift_point = 3000

# Variable to track if the alert window has been shown
alert_shown = False

# Function to show a persistent visual alert window
def show_shift_alert():
    global alert_shown
    
    # Only show the alert once
    if not alert_shown:
        # Create a new Tkinter window
        root = tk.Tk()
        root.title("Shift Alert")

        # Set the window size (optional)
        root.geometry("300x150")

        # Add a label with the alert message
        label = tk.Label(root, text="Time to shift gears!", font=("Arial", 14))
        label.pack(pady=40)

        # Add a button to close the alert window
        close_button = tk.Button(root, text="OK", command=root.destroy)
        close_button.pack(pady=10)

        # Keep the window open until the user clicks OK
        root.mainloop()

        # Mark the alert as shown to avoid reopening it
        alert_shown = True

while True:
    # Get current RPM
    rpm = connection.query(obd.commands.RPM)

    if rpm.is_null():
        print("Unable to read RPM")
    else:
        current_rpm = rpm.value
        print(f"Current RPM: {current_rpm}")

        # Check if it's time to shift
        if current_rpm >= shift_point and not alert_shown:
            show_shift_alert()  # Trigger the visual alert
            
    time.sleep(0.5)  # Delay for half a second before next check
