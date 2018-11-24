from periphery import Serial, GPIO
import re

def treatGNIDString(string):
    return re.sub(r'=ERR|=|\n', "", string.decode('utf-8'))

class SwarmBee:
    def __init__(self):
        return self
    def getID(self):
        return self.call('GNID')
    def setID(self, id):
        return self.call('SNID', id)
    def getDistance(self, nodeId):
        return self.call('RATO', nodeId)

    def call(operation, parameter = None):
        res = None

        pinVCC = GPIO(17, "high")
        pinMOD_EN = GPIO(27, "high")
        pinA_MODE = GPIO(22, "low")
        serial = Serial("/dev/ttyAMA0", baudrate=115200)

        operationWithParameter = operation + " " + parameter + "\r\n"
        operationWithParameter = operationWithParameter.encode('utf-8')

        serial.write(operationWithParameter)
        serial.flush()
        if serial.poll(100):
            inComing = serial.input_waiting()
            buffer = serial.read(inComing, 10)
            res = treatGNIDString(buffer))
        serial.close()
        return res
