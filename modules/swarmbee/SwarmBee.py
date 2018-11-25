from periphery import Serial, GPIO
import re
import time
import subprocess

def treatGNIDString(string):
    return re.sub(r'=ERR|=|\n', "", string.decode('utf-8'))

class SwarmBee:
    def _init_(self, vccPin = 17, modPin = 27, aModePin = 22, ttyPort="/dev/ttyAMA0" ):
        self.vccPin = vccPin
        self.modPin = modPin
        self.aModePin = aModePin
        self.ttyPort = ttyPort
        self.serial = self.buildSerial()
        return self

    def buildSerial(self):
        pinVCC = GPIO( self.vccPin , "high")
        pinMOD_EN = GPIO( self.modPin , "high")
        pinA_MODE = GPIO( self.aModePin , "low")
        serial = Serial( self.ttyPort , baudrate=115200)
        return serial

    def getID(self):
        return self.call('GNID')

    def setID(self, id):
        return self.call('SNID', id)

    def getDistance(self, nodeId):
        return self.call('RATO 0', nodeId)

    def readOnSerial(self):
        res = None
        self.serial.flush()
        if self.serial.poll(100):
            print('Aqui')
            inComing = self.serial.input_waiting()
            buffer = self.serial.read(inComing, 10)
            res = treatGNIDString(buffer)
        self.serial.close()
        return res

    def callCommand(self, operation, parameter = ""):
        subprocess.Popen("sudo chmod 666 "+ self.ttyPort, shell=True)
        
        operationWithParameter = str(operation) + " " + str(parameter) + "\r\n"
        operationWithParameter = operationWithParameter.encode('utf-8')

        self.serial.write(operationWithParameter)
    
    def runProcess(self, operation, parameter = ""):
        self.callCommand(operation, parameter)
        return self.readOnSerial()

    @staticmethod
    def __time_stamp():
        c_time = time.time()
        ms = int(round(c_time * 1000 % 1000))

        time_str = '{}.{:0=3d}'.format(time.strftime('%H:%M:%S'), ms)
        return time_str