from flask import Flask, render_template, redirect, url_for  
import psutil  # import psutil module for process management
import datetime  
from water import * 
import threading 

app = Flask(__name__)  # create a flask application instance
stop_flag = threading.Event()

def template(title="HELLO!", text=""):  
    now = datetime.datetime.now()  
    timeString = now  
    templateDate = {  # create a dictionary to store template data
        'title': title,  
        'time': timeString,
        'text': text  
    }
    return templateDate  

@app.route("/")  # define a route for the root URL
def hello():  # define a function to handle the root URL
    templateData = template()  # generate template data using the template function
    return render_template('main.html', **templateData)  # render the main.html template with the template data

@app.route("/last_watered")  # define a route for the last_watered URL
def check_last_watered():  # define a function to handle the last_watered URL
    templateData = template(text=get_last_watered())  # generate template data with the last watered time
    return render_template('main.html', **templateData)  # render the main.html template with the template data

@app.route("/sensor")  
def action(): 
    status = get_status()  
    message = "" 
    if (status == 1):  #sensor = dry
        message = "Water me please!"  
    else: 
        message = "I'm a happy plant" 
    templateData = template(text=message) 
    return render_template('main.html', **templateData)  

@app.route("/water")  
def action2():  
    pump_on()  
    templateData = template(text="Watered Once")  
    return render_template('main.html', **templateData)  
@app.route("/auto/water/<toggle>")
def auto_water_button(toggle):
    global stop_flag # threading event
    if toggle == "ON":
        if get_status() == 0:
            templateData = template(text="Already watered. Auto-watering not started.")
        else:
            stop_flag.clear() # clears stop watering flag and starts new auto watering thread
            auto_water_thread = threading.Thread(target=auto_water, kwargs={'delay': 5, 'stop_flag': stop_flag})
            auto_water_thread.start()
            templateData = template(text="Auto Watering On")
    else:
        stop_flag.set() # auto watering thread stops
        pump_off()
        templateData = template(text="Auto Watering Off")
    return render_template('main.html', **templateData)
try:
    if __name__ == "__main__":  # if the script is run directly (not imported as a module)
        app.run(host='192.168.0.210', debug=True)  
except KeyboardInterrupt:
   init.pins()
