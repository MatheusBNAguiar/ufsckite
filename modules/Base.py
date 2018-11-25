from swarmbee import SwarmBee, SwarmNode

class Base:
    def __init__(self, nodeId):
        RATO_FILE = r"./rato" + str(nodeId) + ".txt"
        self.swarm = SwarmBee()
        self.nodeId = nodeId
        self.file = open(RATO_FILE, 'w')

    def getDistance(self, node):
        return self.swarm.getDistance(node)

    def getSettings(self):
        return self.swarm.getSettings()

    def getId(self):
        return self.swarm.getID()
    # def setId(self):