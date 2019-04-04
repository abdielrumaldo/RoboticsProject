import pygame, sys, time
import serial
import RPi.GPIO as GPIO

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

def getDistance1():

    # Send ping
#print('sending ping')
    GPIO.output(TRIG1, False)
    time.sleep(.01)
    GPIO.output(TRIG1, True)
    time.sleep(.01)
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

    # Send ping
   # print('starting ping')
    GPIO.output(TRIG2, False)
    time.sleep(.01)
    GPIO.output(TRIG2, True)
    time.sleep(.01)
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
       


ser = serial.Serial(
    port = '/dev/serial0',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
    )


display_width = 100
display_height = 100

gameDisplay = pygame.display.set_mode((display_width, display_height))

clock = pygame.time.Clock()

main = True
while main == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            main = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move = '!S 1 1000_!S 2 -1000_'.encode('utf-8')
                ser.write(move)
                print(move)
            if event.key == pygame.K_RIGHT:
                move = '!S 1 -1000_!S 2 1000_'.encode('utf-8')
                ser.write(move)
                print(move)
            if event.key == pygame.K_UP:
                move = '!S 1 1000_!S 2 1000_'.encode('utf-8')
                ser.write(move)
                print(move)
            if event.key == pygame.K_DOWN:
                move = '!S 1 -1000_!S 2 -1000_'.encode('utf-8')
                ser.write(move)
                print(move)
            if event.key == pygame.K_DOWN:
                move = '!S 1 -1000_!S 2 -1000_'.encode('utf-8')
                ser.write(move)
                print(move)
            if event.key == ord('a'):
                command = '!S 1 10000_!S 2 -10000_'.encode('utf-8')
                ser.write(command)
                print(command)
        

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                command = '!S 1 0_!S 2 0_'.encode('utf-8')
                ser.write(command)
                print(command)
            if event.key == pygame.K_RIGHT:
                command = '!S 1 0_!S 2 0_'.encode('utf-8')
                ser.write(command)
                print(command)
            if event.key == pygame.K_LEFT:
                command = '!S 1 0_!S 2 0_'.encode('utf-8')
                ser.write(command)
                print(command)
            if event.key == pygame.K_DOWN:
                command = '!S 1 0_!S 2 0_'.encode('utf-8')
                ser.write(command)
                print(command)
            if event.key == ord('a'):
                command = '!S 1 0_!S 2 0_'.encode('utf-8')
                ser.write(command)
                print(command)
            

            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                main = False
                
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
