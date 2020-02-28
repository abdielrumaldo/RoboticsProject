# ===============================Raspi Configuration=====================================
import RPi.GPIO as GPIO
import json

'''
    This is the setup that is required in order to communicate and retieve
    information from the sonar device.

    Used Imports: 
    import RPi.GPIO as GPIO

    Source information
    https://learn.sparkfun.com/tutorials/raspberry-gpio/all
'''
# Values may change accoridng to the ports available on the PI
# Reads configuration form the config.json file
def raspiInit():
    """
    Initialize the python pins for raspi sonar from the config.json
    """
    with open ('config.json') as configurationFile:
        data = json.load(configurationFile)
        config = data['config'][0]

        print("Printing current config")
        for key, value in config.items():
            print("{} : {}".format(key, value))

    GPIO.setmode(GPIO.BCM) #  activate the Broadcom-chip specific pin numbers. Required for Python.
    GPIO.setwarnings(False)

    # Set the input pins
    GPIO.setup(config['SIG1'], GPIO.OUT)
    GPIO.setup(config['TRIG1'],GPIO.OUT)
    GPIO.setup(config['SIG2'], GPIO.OUT)
    GPIO.setup(config['TRIG2'],GPIO.OUT)


    # Set the output pins
    GPIO.setup(config['ECHO2'],GPIO.IN)
    GPIO.setup(config['ECHO1'],GPIO.IN)
    GPIO.setup(config['WARN'], GPIO.IN)

    GPIO.output(config['SIG1'], True)
    GPIO.output(config['SIG1'], True)


#===============================================================================================