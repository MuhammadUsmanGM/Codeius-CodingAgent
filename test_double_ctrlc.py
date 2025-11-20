"""
Test script to demonstrate the double Ctrl+C functionality.
This is only for demonstration - the actual implementation is in cli.py
"""
import time
import signal
import sys

def signal_handler(signum, frame):
    """Handle Ctrl+C (SIGINT) signals"""
    global first_ctrl_c_time
    
    current_time = time.time()
    
    # Check if the first Ctrl+C happened less than 2 seconds ago
    if first_ctrl_c_time is not None and (current_time - first_ctrl_c_time) < 2.0:
        # Second Ctrl+C detected - exit now
        print("\nDouble Ctrl+C detected – exiting immediately...")
        sys.exit(0)
    else:
        # First Ctrl+C - set the timer and warn the user
        first_ctrl_c_time = current_time
        print("\nCtrl+C detected – press again within 2 seconds to exit")
        # Continue the program

# Initialize the variable
first_ctrl_c_time = None

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

print("Test program for double Ctrl+C functionality")
print("Press Ctrl+C once to see the warning")
print("Press Ctrl+C again within 2 seconds to exit")
print("If more than 2 seconds pass, only the first Ctrl+C will be registered")
print("\nRunning... Press Ctrl+C to test:")

try:
    while True:
        time.sleep(0.1)  # Simulate some work
        print(".", end="", flush=True)
except KeyboardInterrupt:
    print("\nProgram interrupted")
except SystemExit:
    print("\nProgram exited normally")