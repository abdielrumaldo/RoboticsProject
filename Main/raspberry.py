# ===============================Raspi Configuration=====================================
#import RPi.GPIO as GPIO
import json

'''
    This is the setup that is required in order to communicate and retieve
    information from the sonar device.

    Used Imports: 
    import RPi.GPIO as GPIO

    Source information
    https://learn.sparkfun.com/tutorials/raspberry-gpio/all

    Config File Format:

    {
    "config": [
        {
        "TRIG1" : 23,
        "ECHO1" : 24,
        "SIG1" : 18,
        "WARN" : 25,
        "TRIG2" : 17,
        "ECHO2" : 27,
        "SIG2" : 18
        }
    ]
    }

'''
# Values may change accoridng to the ports available on the PI
# Reads configuration form the config.json file
#===============================================================================================

class Sonar:
    def __init__(self, fileName):
        """
        Initialize the python pins for raspi sonar from the config.json
        """
        with open (fileName) as configjson:
            data = json.load(configjson)
            self.config = data["config"][0]


        # GPIO.setmode(GPIO.BCM) #  activate the Broadcom-chip specific pin numbers. Required for Python.
        # GPIO.setwarnings(False)

        # Set the input pins
        # GPIO.setup(config['SIG1'], GPIO.OUT)
        # GPIO.setup(config['TRIG1'],GPIO.OUT)
        # GPIO.setup(config['SIG2'], GPIO.OUT)
        # GPIO.setup(config['TRIG2'],GPIO.OUT)


        # Set the output pins
        # GPIO.setup(config['ECHO2'],GPIO.IN)
        # GPIO.setup(config['ECHO1'],GPIO.IN)
        # GPIO.setup(config['WARN'], GPIO.IN)

        # GPIO.output(config['SIG1'], True)
        # GPIO.output(config['SIG1'], True)

        
    def printConfig(self):

        print("PrintingConfiguration file")

        for key, value in self.config.items():
            print("{} : {}".format(key, value))

    def getDistance(self):

        # Send ping
        #print('sending ping')
        GPIO.output(TRIG1, False)
        time.sleep(.0001)
        GPIO.output(TRIG1, True)
        time.sleep(.00001)
        GPIO.output(TRIG1, False)

        #print('Getting Ping')
        # Get the time between pings
        while GPIO.input(ECHO1) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO1) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = (pulse_duration * 17000)/2 - (pulse_duration * 17000)/11
        distance = round(distance, 2)
        
        return distance

    def viewFront(self, port):
        '''
        See if the front is blocked
        '''
            
        while GPIO.input(25) == 0:
            print('Pausing')
            #STARTMOVE = '!S 1 0_!S 2 {}_'.format(0).encode('utf-8')
            #port.write(STARTMOVE)
            time.sleep(1)