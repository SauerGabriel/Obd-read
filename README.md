# Obd-read
Python script to read obd data and print on screen

# OBD-II Gear and Turbo Monitor

This project monitors the RPM, gear, and turbo pressure of my 2012 Mitsubishi Lancer Ralliart using an OBD-II adapter and provides a GUI interface.

## Features
- Displays RPM, gear, and turbo pressure.
- Alerts when RPM exceeds the set threshold.
- Adjustable RPM warning threshold via the GUI.

## Requirements
- Python 3.x
- OBD-II Bluetooth/USB adapter.
- `python-OBD` library.

## Installation
1. Install Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Install dependencies:
   ```bash
   pip install obd
