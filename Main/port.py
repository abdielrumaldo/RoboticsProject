import serial

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