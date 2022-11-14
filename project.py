# kurtis bertauche
# cpe 400 project
# project.py

# libraries

class Packet:
    def __init__(self, destination):
        self.destination = destination   
    visitedRouters = []

class Router:
    def __init__(self, key, energy):
        self.key = key
        self.energy = energy
        self.alive = True
        if(energy < 0):
            self.alive = False
    
    queue = []

    def receivePacket(self, packet):
        self.queue.append(packet)

    def transmitPacket(self):
        frontPacket = self.queue[0]
        self.queue.popleft()
        frontPacket.visitedRouters.append(self.key)
        energy = energy - 1
        if(energy < 0):
            self.alive = False
        return frontPacket

    def getNextPacketDestination(self):
        return self.queue[0].destination

# begin of main
# read in file of nodes and connections
globalView = {}

file = open("network_one.csv", "r")
for x in file:
    x = x.split(",")
    x[-1] = x[-1].replace('\n', "")
    globalView[x[0]] = x[1:]

print(globalView["a"])



