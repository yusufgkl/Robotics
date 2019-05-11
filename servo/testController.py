import serial
import time

class ServoController:
    def __init__(self):
        usbPort = '/dev/tty.usbmodem002475011'
        self.sc = serial.Serial(usbPort, timeout=1)

    def closeServo(self):
        self.sc.close()

    def setAngle(self, n, angle):
        # if angle > 180 or angle <0:
        #    angle=90
        
        if angle > 0:
            angle = angle - 15

        if (angle >= 180):
            print('IOYFDGIDF')
            angle = 150
        
        
        byteone=int(254*angle/180)
        bud=chr(0xFF)+chr(n)+chr(byteone)
        self.sc.write(bud)

    def setPosition(self, servo, position):
        position = position * 4
        poslo = (position & 0x7f)
        poshi = (position >> 7) & 0x7f
        chan  = servo &0x7f
        data =  chr(0xaa) + chr(0x0c) + chr(0x04) + chr(chan) + chr(poslo) + chr(poshi)
        self.sc.write(data)

    def getPosition(self, servo):
        chan  = servo &0x7f
        data =  chr(0xaa) + chr(0x0c) + chr(0x10) + chr(chan)
        self.sc.write(data)
        w1 = ord(self.sc.read())
        w2 = ord(self.sc.read())
        return w1, w2

    def getErrors(self):
        data =  chr(0xaa) + chr(0x0c) + chr(0x21)
        self.sc.write(data)
        w1 = ord(self.sc.read())
        w2 = ord(self.sc.read())
        return w1, w2

    def triggerScript(self, subNumber):
        data =  chr(0xaa) + chr(0x0c) + chr(0x27) + chr(0)
        self.sc.write(data)
    
    def set_speed(self,servo,speed):
        chan  = servo &0x7f
        data = chr(0xaa) + chr(0x0c) + chr(0x07) + chr(chan) + chr(speed & 0x7f) + chr((speed >> 7) & 0x7f)
        self.sc.write(data)

servo = ServoController()
sleepTime = 2
num = 3
i = 0

while (i != num):
    servo.set_speed(i, 5)
    servo.setAngle(i, 90)
    i = i + 1

print(servo.getErrors())
servo.closeServo()