# ===============================Raspi Configuration=====================================
#import RPi.GPIO as GPIO
import json
import os
print (os.getcwd())
'''
    This is the setup that is required in order to communicate and retieve
    information from the sonar device.

    Used Imports: 
    import RPi.GPIO as GPIO

    Source information
    https://learn.sparkfun.com/tutorials/raspberry-gpio/all
'''
# Values may change accoridng to the ports available on the PI
# This can be moved to a configuration file to be edited
with open ('config.json') as configurationFile:
    data = json.load(configurationFile)
    for p in data["config"]:
        print("Config: {}".format(p))
#config = 


#print("Initializing Raspeverry PI conofig\n")

#config = "\nTRIG1 = pin {}\nECHO1 = pin {}\nSIG1 = pin {}\nWARN = pin {}\nTRIG2 = pin {}\nECHO2 = pin {}\nSIG2 = pin {}\n".format(TRIG1,ECHO1,SIG1,WARN,TRIG2,ECHO2,SIG2)
#print("Configuration: \n{}".format(config))

GPIO.setmode(GPIO.BCM) #  activate the Broadcom-chip specific pin numbers. Required for Python.
GPIO.setwarnings(False)

# Set the input pins
GPIO.setup(SIG1, GPIO.OUT)
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(SIG2, GPIO.OUT)
GPIO.setup(TRIG2,GPIO.OUT)


# Set the output pins
GPIO.setup(ECHO2,GPIO.IN)
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(WARN, GPIO.IN)

GPIO.output(SIG1, True)
GPIO.output(SIG1, True)
#===============================================================================================