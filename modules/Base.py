from swarmbee import SwarmBee, SwarmNode

class Base:
    def __init__(self, nodeId):
        RATO_FILE = r"./rato" + str(nodeId) + ".txt"
        
        self.swarm = SwarmNode('/dev/ttyAMA0', True, True)
        self.swarm.open_port()
        self.nodeId = nodeId
        self.file = open(RATO_FILE, 'w')

    def getDistance(self, node):
        self.swarm.ranging(node)
        self.swarm.process_buf(self.file)

    def getId(self):
        return self.swarm.getNodeId()
    # def setId(self):