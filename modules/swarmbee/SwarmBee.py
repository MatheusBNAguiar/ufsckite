from periphery import Serial, GPIO
import re
import subprocess

def treatGNIDString(string):
    return re.sub(r'=ERR|=|\n', "", string.decode('utf-8'))

class SwarmBee:
    def _init_(self, vccPin, modPin, aModePin, ttyPort):
        self.vccPin = vccPin
        self.modPin = modPin
        self.aModePin = aModePin
        self.ttyPort = ttyPort
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

    def call(self, operation, parameter = ""):
        subprocess.Popen("sudo chmod 666 "+ self.ttyPort, shell=True)
        res = None
        serial =  self.buildSerial()
        
        operationWithParameter = str(operation) + " " + str(parameter) + "\r\n"
        operationWithParameter = operationWithParameter.encode('utf-8')

        serial.write(operationWithParameter)
        print(operationWithParameter)
        serial.flush()
        if serial.poll(100):
            print('Aqui')
            inComing = serial.input_waiting()
            buffer = serial.read(inComing, 10)
            res = treatGNIDString(buffer)
        serial.close()
        return res