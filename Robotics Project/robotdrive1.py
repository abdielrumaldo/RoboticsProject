import RPi.GPIO as GPIO
import time
import serial
import atexit
import map

locations = map.map

def nextHop(current_position):
    next_hop = current_position['nextHop']
    return next_hop
    
def getDistance1():

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

def getLocation(port):
	
        flush = port.read(100)
	command = b'?C 1_'
	port.write(command)

	message = port.read(100)
	message = message[7:-1].decode('ascii')
	message = int(message)
	return message
	'''
	print('Initial has been set to {} units'.format(init))
	move = '!S 1 500_!S 2 500_'.encode('utf-8')
	port.write(move)
	port.read(100)
	
	dump = input('Destination: Press \"Enter\" to stop')
	
	command = b'?C 1_'
	port.write(command)
	
	message = port.read(100)
	message = message[7:-1].decode('ascii')
	message = int(message)
	fin = message
	print('Final has been set to {} units'.format(fin))
	
	total = fin - init
	print('You have moved a total of {} units'.format(total))
	'''


def getDistance2():

    # Send ping
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
       

def startup(port, locations):
    '''
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

    current_location = getLocation()
    values.append(current_location)
    
    pos_start = 1
    first_hop = locations[pos_start]
    values.append(first_hop)
    
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

    well = True
    while well:

        print('Checking Front')
        while 1:
            viewFront(port)
        print('Front Clear')
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

    
def robotAlign(port):
    
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

'''
    This is the setup that is required in order to communicate and retieve
    information from the sonar device.
'''
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Values may change accoridng to the ports available on the PI
TRIG1 = 23
ECHO1 = 24
SIG1 = 18
WARN = 25

GPIO.setup(SIG1, GPIO.OUT)
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(WARN, GPIO.IN)

GPIO.output(SIG1, True)

TRIG2 = 17
ECHO2 = 27
SIG2 = 18

GPIO.setup(SIG2, GPIO.OUT)
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)

GPIO.output(SIG1, True)

print('starting programs')
#values = startup()
values = [12,40,35]
wallFollow(ser, values)
#start-position = start()
try: 
	
	#STARTMOVE = '!S 1 1000_!S 2 {}_'.format(500).encode('utf-8')
	#ser.write(STARTMOVE)
    '''
	while 1:
		start(ser)
		temp = input('Press enter to continue')
    '''
    values = startup()
    wallFollow(ser, values)
except (KeyboardInterrupt, SystemExit):
    print('Stopping Robot!')
    command = '!S 1 0_!S 2 0_'.encode('utf-8')
    ser.write(command)

