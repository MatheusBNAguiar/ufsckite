#liga

class Measurement():
    def __init__(self, senderModule, receiverModule):
        self.receiverModule = receiverModule
        self.senderModule = senderModule
    def getDistance(self):
        # get distance swarm bee
        self.distance = SwarmBee.getDistance(receiverModule)
    def storeDistance(self)
        #store on txt
        time = SwarmBee.getTimeStamp()
        TXT.append(time, senderModule, receiverModule, self.distance)
    def calculateDistance(self)
        distance = self.getDistance()
        self.storeDistance(distance)

class Module():
    def __init__(self):
        self.measurementsInstances = []

    def setupDistance(self):
        droneId = '000000000001'
        masterId = '000000000002'
        slaveIds = ['000000000003', '000000000004', '000000000005', '000000000006']

        # cria instancias de measurement
        for(i in range(len(slaveIds))):
            self.measurementsInstances.push(Measurement(ownId, slaveIds[i]))
        self.measurementsInstances.push(Measurement(ownId, masterId))

        self.triggerDistance()

    def triggerDistance(self):
        for(measurement in self.measurementInstances):
            measurement.calculateDistance()

#espera comando master
## espera receber


    # inicia buzina


    #emite som
    a = Module()
    a.setupDistance()

    



