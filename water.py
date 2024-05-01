import RPi.GPIO as GPIO
import datetime 
import time

init = False 
GPIO.setmode(GPIO.BOARD) 

pump_pin = 15
sensor_pin = 8

# Function to get the last watered time from a file
def get_last_watered():
    try:
        f = open("last_watered.txt", "r")  # Open the file in read mode
        return f.readline()  # Read the first line of the file and return it
    except:
        return "NEVER!"  # If the file doesn't exist or an error occurs, return "NEVER!"

# Function to get the status of a sensor connected to a specific pin
def get_status(): 
      # Set the specified pin as an input 
    return GPIO.input(sensor_pin)  # Read and return the value of the specified pin

# Function to initialize an output pin
GPIO.setup(sensor_pin, GPIO.IN)
GPIO.setup(pump_pin, GPIO.OUT)  # Set the pin as an output
GPIO.output(pump_pin, GPIO.LOW)

# Function to automatically water the plant based on sensor readings
def auto_water(delay=0, stop_flag=None):
    print("Auto-watering started. Press CTRL+C to exit.")
    while not stop_flag.is_set():
        wet = get_status() == 0
        if not wet:
            pump_on(duration=10)  
            time.sleep(delay)
        else:
            print("Sensor is wet, waiting for it to dry...") #delay to chk if sensor wet
            time.sleep(delay)
    print("Auto-watering stopped.")

# Function to turn on the pump for a specified duration
def pump_on(duration=1):
    f = open("last_watered.txt", "w")  # Open the last_watered.txt file in write mode
    f.write("Last watered {}".format(datetime.datetime.now()))  # Write the current date and time to the file
    f.close()  # Close the file
    GPIO.output(pump_pin, GPIO.HIGH)  # Turn on the pump by setting the pin to LOW
    time.sleep(duration)  # Wait for the specified delay (default is 1 second)
    GPIO.output(pump_pin, GPIO.LOW)  # Turn off the pump by setting the pin to HIGH

def pump_off():
    print("turning off here with pin ", pump_pin)
    GPIO.output(pump_pin, GPIO.LOW)
	#GPIO.cleanup()
    
	#GPIO.setmode(GPIO.BOARD) 
 

def init_pins():
    GPIO.setup(sensor_pin, GPIO.IN)
    GPIO.setup(pump_pin, GPIO.OUT)  # Set the pin as an output
    GPIO.output(pump_pin, GPIO.LOW)

# Main function
# try:
#    while True:
#        print("Select an option:")
#        print("1. Auto Watering")
#        print("2. Manual Watering")
#        print("3. Exit")
#        choice = input("Enter your choice: ")
        
#        if choice == 1:
#            auto_water()
#        elif choice == 2:
#            pump_on()
#            print("Manual watering started.")
#            time.sleep(1)  # Ensuring the pump runs for at least 1 second
#            pump_off()
#            print("Manual watering stopped.")
#        elif choice == 3:
#            break
#        else:
#            print("Invalid choice. Please enter a valid option.")
# except KeyboardInterrupt:
#    GPIO.cleanup()

