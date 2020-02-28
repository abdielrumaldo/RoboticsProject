import RPi.GPIO as GPIO
import time
import serial
import atexit
import map

# ============TODO===============

""" 


Move the configurations to human readable configuration files that can be changed. DONE

Turn the sonars into classes? Probably allows for modular user of them.

Document code -in progress-

Create log files and a logging system instead of outputting to console

add a naming scheme

"""

# ===============================Raspi Configuration=====================================
'''
    This is the setup that is required in order to communicate and retieve
    information from the sonar device.

    Used Imports: 
    import RPi.GPIO as GPIO
'''
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Values may change accoridng to the ports available on the PI
# This can be moved to a configuration file to be edited
TRIG1 = 23
ECHO1 = 24
SIG1 = 18
WARN = 25
TRIG2 = 17
ECHO2 = 27
SIG2 = 18


GPIO.setup(SIG1, GPIO.OUT)
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(WARN, GPIO.IN)

GPIO.output(SIG1, True)


GPIO.setup(SIG2, GPIO.OUT)
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)

GPIO.output(SIG1, True)
#===============================================================================================


#========================================Serial Interface Configuration============================================

'''
    This creates the object ser which is the means of trasmission between 
    the raspberry pi and the controller.
'''

ser = serial.Serial(
    port = '/dev/serial0',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
    )
#===============================================================================================

#========================================Functions============================================

# This is used to create a copy of the "map" which contains all the locations the robot can go to
locations = map.map



def nextHop(current_position): 
    """ 
    This function is meant to pull the location of the next location in the 'map'
    """
    next_hop = current_position['nextHop']
    return next_hop
    

def getDistance1():
    """ 
    This function returns the distance using sonar
    """

    # Send ping WHY IS THIS NOT A FUNCTION!?!?

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

def getDistance2():

    """ 
    This function returns the distance using sonar
    """

    # Send ping AGAIN WHY IS THIS NOT A FUNCTION
   # print('starting ping')
    GPIO.output(TRIG2, False)
    time.sleep(.0001)
    GPIO.output(TRIG2, True)
    time.sleep(.00001)
    GPIO.output(TRIG2, False)
   # print('Ping Recieved')
    # Get the time between pings
    while GPIO.input(ECHO2) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO2) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
   # print('calculating distance')
    distance = (pulse_duration * 17000)/2 - (pulse_duration * 17000)/11
    distance = round(distance, 2)
    #print('Returning distance')
    
    return distance
       

def getLocation(port):
    """ 
    This function returns the distance stored within the robot/controller
    """

    flush = port.read(100)
    command = b'?C 1_'
    port.write(command)
    
    message = port.read(100)
    print(message)
    message = message[7:-1].decode('ascii')
    print(message)
    message = int(message)
    return message


def startup(port, locations):
    '''
    input description
    Values = [Threshold, minimum, max,current_location , next hop distance]
    '''
    values = []
    rearReading = getDistance1()
    frontReading = getDistance2()

    threshold = 2
    values.append(threshold)
    
    minimmum = rearReading - threshold
    values.append(minimmum)
    
    maximum = rearReading + threshold
    values.append(maximum)

    current_location = getLocation(port)
    values.append(current_location)
    
    pos_start = 1
    first_hop = locations[pos_start]
    distance = first_hop['distance']
    values.append(distance)
    
    return values


def pidVar(values):
    '''
        Should control the left wheel, the closer to the wall the more aggressive the turn
        Requires startup to run first
        Values = [Threshold, minimum, max]
    '''
    frontReading = getDistance2() 

    if frontReading >= values[1]:
        holder = 1000
    else:
        dx = frontReading - (values[2] - values[0])
        dx = (dx * dx)
        return 1000 - dx
    
    if frontReading <= values[2]:
        holder = 1000
    else:
        dx = frontReading - (values[2] - values[0])
        dx = (dx * dx) 
        return 1000 + dx
    
    return holder

def viewFront(port):
    '''
    See if the front is blocked
    '''
        
    while GPIO.input(25) == 0:
        print('Pausing')
        #STARTMOVE = '!S 1 0_!S 2 {}_'.format(0).encode('utf-8')
        #port.write(STARTMOVE)
        time.sleep(1)
  

    
def wallFollow(port, values):
    '''
    Adjust the speed of the wheel according to the distace from the wall
    Values = [Threshold, minimum, max,current_location , next hop distance]
    '''
    values[3] = getLocation(port)
    far = values[3] + values[4]
    while values[3] <= far:

        viewFront(port)
        STARTMOVE = '!S 1 1000_!S 2 {}_'.format(pidVar(values)).encode('utf-8')
        port.write(STARTMOVE)

        backReading = getDistance1()
        frontReading = getDistance2()
        if frontReading > backReading:
            delta = frontReading - backReading
        
        if backReading > frontReading:
            delta = backReading - frontReading
        
        if delta > 10:
            robotAlign(port)
        values[3] = getLocation(port)
        viewFront(port)
    
    STOPMOVE = '!S 1 0_!S 2 {}_'.format(0).encode('utf-8')
    port.write(STOPMOVE)
    time.sleep(5)
    
def robotAlign(port):
    
    '''
    Stops the robot and re-aligns it when it's too close the wall
    Values = [Threshold, minimum, max,current_location , next hop distance]
    '''
    
    print("Starting Alignment")
    command = '!S 1 0_!S 2 0_'.encode('utf-8')
    port.write(command)
    
    backReading = getDistance1()
    frontReading = getDistance2()

    print('getting information')
    print('Front : {} '.format(frontReading))
    print('Rear : {} '.format(backReading))
    if frontReading > backReading:
        ratio = frontReading / backReading
        print(str(ratio))
        command = '!S 1 0_!S 2 25_'.encode('utf-8')
        port.write(command)
        while ratio >= 1.00:
             frontReading = getDistance2() 
             backReading = getDistance1()
             ratio = frontReading / backReading
             print(str(ratio))
        command = '!S 1 0_!S 2 0_'.encode('utf-8')
        port.write(command)
    
    if frontReading < backReading:
        ratio = frontReading / backReading
        command = '!S 1 0_!S 2 -25_'.encode('utf-8')
        port.write(command)
        while ratio <= 1.00:
             frontReading = getDistance2() 
             backReading = getDistance1()
             ratio = frontReading / backReading
        command = '!S 1 0_!S 2 0_'.encode('utf-8')
        port.write(command)

    backReading = getDistance1()
    frontReading = getDistance2()

    if frontReading > backReading:
        delta = frontReading - backReading

        if delta > 3.5:
            command = '!S 1 0_!S 2 25_'.encode('utf-8')
            port.write(command)
            time.sleep(1)
            command = '!S 1 0_!S 2 0_'.encode('utf-8')
            port.write(command)
    
    if backReading > frontReading:
        delta = backReading - frontReading

        if delta > 3.5:
            command = '!S 1 0_!S 2 25_'.encode('utf-8')
            port.write(command)
            time.sleep(1)
            command = '!S 1 0_!S 2 0_'.encode('utf-8')
            port.write(command)

def STOP(port):
    print('Stopping')
    STOPMOVE = '!S 1 0_!S 2 0_'.encode('utf-8')
    port.write(STOPMOVE)

# ==============================Main program==============================================
""" Init """
print('starting programs')
#values = startup()
#wallFollow(ser, values)
#start-position = start()
values = startup(ser, locations)
current_pos = locations[1]


try: 
	
	#STARTMOVE = '!S 1 1000_!S 2 {}_'.format(500).encode('utf-8')
	#ser.write(STARTMOVE)
    '''
	while 1:
		start(ser)
		temp = input('Press enter to continue')
    '''
    while current_pos['direction'] == 3:
        wallFollow(ser, values)
        current_pos = nextHop(current_pos)
        values[4].update(current_pos['distance'])
    #turn
except (KeyboardInterrupt, SystemExit):
    print('Stopping Robot!')
    command = '!S 1 0_!S 2 0_'.encode('utf-8')
    ser.write(command)

