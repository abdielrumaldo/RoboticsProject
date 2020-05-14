from port import ser as port 

class robot:
    '''
    '''
    def __init__(self, port):
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

    def getLocation(self, port):
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

    def pidVar(self, values):
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

    def viewFront(self, port):
        '''
        See if the front is blocked
        '''
            
        while GPIO.input(25) == 0:
            print('Pausing')
            #STARTMOVE = '!S 1 0_!S 2 {}_'.format(0).encode('utf-8')
            #port.write(STARTMOVE)
            time.sleep(1)
    

        
    def wallFollow(self, port, values):
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
        
    def robotAlign(self, port):
        
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
