# External module imp
import RPi.GPIO as GPIO  # Import the RPi.GPIO module for controlling GPIO pins
import datetime  # Import the datetime module for working with dates and times
import time  # Import the time module for adding delays

init = False  # Initialize a variable to track initialization status
GPIO.setmode(GPIO.BOARD)  # Set the pin numbering scheme to BOARD

# Function to get the last watered time from a file
def get_last_watered():
    try:
        f = open("last_watered.txt", "r")  # Open the file in read mode
        return f.readline()  # Read the first line of the file and return it
    except:
        return "NEVER!"  # If the file doesn't exist or an error occurs, return "NEVER!"

# Function to get the status of a sensor connected to a specific pin
def get_status(pin=8):
    GPIO.setup(pin, GPIO.IN)  # Set the specified pin as an input
    return GPIO.input(pin)  # Read and return the value of the specified pin

# Function to initialize an output pin
def init_output(pin):
    GPIO.setup(pin, GPIO.OUT)  # Set the specified pin as an output
    GPIO.output(pin, GPIO.LOW)  # Set the specified pin to LOW
    GPIO.output(pin, GPIO.HIGH)  # Set the specified pin to HIGH

# Function to automatically water the plant based on sensor readings
def auto_water(delay=5, pump_pin=7, water_sensor_pin=8):
    consecutive_water_count = 0  # Initialize a counter for consecutive water readings
    init_output(pump_pin)  # Initialize the pump pin as an output
    print("Here we go! Press CTRL+C to exit")  # Print a message to indicate the start of the loop
    try:
        while 1 and consecutive_water_count < 10:  # Loop indefinitely until the consecutive water count reaches 10
            time.sleep(delay)  # Wait for the specified delay
            wet = get_status(pin=water_sensor_pin) == 0  # Check if the water sensor pin is wet (returns 0 when wet)
            if not wet:  # If the sensor is not wet
                if consecutive_water_count < 5:  # If the consecutive water count is less than 5
                    pump_on(pump_pin, 1)  # Turn on the pump for 1 second
                    consecutive_water_count += 1  # Increment the consecutive water count
            else:
                consecutive_water_count = 0  # Reset the consecutive water count if the sensor is wet
    except KeyboardInterrupt:
        # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup()  # Clean up all GPIO pins

# Function to turn on the pump for a specified duration
def pump_on(pump_pin=7, delay=1):
    init_output(pump_pin)  # Initialize the pump pin as an output
    f = open("last_watered.txt", "w")  # Open the last_watered.txt file in write mode
    f.write("Last watered {}".format(datetime.datetime.now()))  # Write the current date and time to the file
    f.close()  # Close the file
    GPIO.output(pump_pin, GPIO.LOW)  # Turn on the pump by setting the pin to LOW
    time.sleep(1)  # Wait for the specified delay (default is 1 second)
    GPIO.output(pump_pin, GPIO.HIGH)  # Turn off the pump by setting the pin to HIGH