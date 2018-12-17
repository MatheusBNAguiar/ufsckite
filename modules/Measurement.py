class Measurement():
    def __init__(self, senderModule, receiverModule):
        self.receiverModule = receiverModule
        self.senderModule = senderModule
    def getDistance(self):
        # get distance swarm bee
        self.distance = SwarmBee.getDistance(receiverModule)
    def storeDistance(self):
        time = SwarmBee.getTimeStamp()
        TXT.append(time, senderModule, receiverModule, self.distance)
    def calculateDistance(self):
        distance = self.getDistance()
        self.storeDistance(distance)