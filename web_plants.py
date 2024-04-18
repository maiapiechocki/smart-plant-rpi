from flask import Flask, render_template, redirect, url_for  # import necessary modules from flask
import psutil  # import psutil module for process management
import datetime  # import datetime module for working with dates and times
import water  # import custom water module
import os  # import os module for interacting with the operating system

app = Flask(__name__)  # create a flask application instance

def template(title="HELLO!", text=""):  # define a function to generate template data
    now = datetime.datetime.now()  # get the current date and time
    timeString = now  # assign the current time to a variable
    templateDate = {  # create a dictionary to store template data
        'title': title,  # set the title in the template data
        'time': timeString,  # set the time in the template data
        'text': text  # set the text in the template data
    }
    return templateDate  # return the template data dictionary

@app.route("/")  # define a route for the root URL
def hello():  # define a function to handle the root URL
    templateData = template()  # generate template data using the template function
    return render_template('main.html', **templateData)  # render the main.html template with the template data

@app.route("/last_watered")  # define a route for the last_watered URL
def check_last_watered():  # define a function to handle the last_watered URL
    templateData = template(text=water.get_last_watered())  # generate template data with the last watered time
    return render_template('main.html', **templateData)  # render the main.html template with the template data

@app.route("/sensor")  # define a route for the sensor URL
def action():  # define a function to handle the sensor URL
    status = water.get_status()  # get the status from the water module
    message = ""  # initialize an empty message variable
    if (status == 1):  # if the status is 1
        message = "Water me please!"  # set the message to indicate watering is needed
    else:  # if the status is not 1
        message = "I'm a happy plant"  # set the message to indicate the plant is happy
    templateData = template(text=message)  # generate template data with the message
    return render_template('main.html', **templateData)  # render the main.html template with the template data

@app.route("/water")  # define a route for the water URL
def action2():  # define a function to handle the water URL
    water.pump_on()  # call the pump_on function from the water module
    templateData = template(text="Watered Once")  # generate template data with a watering message
    return render_template('main.html', **templateData)  # render the main.html template with the template data

@app.route("/auto/water/<toggle>")  # define a route for the auto water URL with a toggle parameter
def auto_water(toggle):  # define a function to handle the auto water URL
    running = False  # initialize a variable to track if auto watering is running
    if toggle == "ON":  # if the toggle is set to "ON"
        templateData = template(text="Auto Watering On")  # generate template data with an "Auto Watering On" message
        for process in psutil.process_iter():  # iterate over all running processes
            try:
                if process.cmdline()[1] == 'auto_water.py':  # if a process is running 'auto_water.py'
                    templateData = template(text="Already running")  # generate template data with an "Already running" message
                    running = True  # set the running variable to True
            except:
                pass  # ignore any exceptions and continue the loop
        if not running:  # if auto watering is not already running
            os.system("python3.4 auto_water.py&")  # start the auto_water.py script in the background
    else:  # if the toggle is not set to "ON"
        templateData = template(text="Auto Watering Off")  # generate template data with an "Auto Watering Off" message
        os.system("pkill -f water.py")  # kill any running water.py processes
    return render_template('main.html', **templateData)  # render the main.html template with the template data

if __name__ == "__main__":  # if the script is run directly (not imported as a module)
    app.run(host='0.0.0.0', port=80, debug=True)  # run the flask application on host 0.0.0.0, port 80, with debug mode enabled