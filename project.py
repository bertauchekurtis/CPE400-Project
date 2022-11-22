# kurtis bertauche
# cpe 400 project
# project.py

# libraries

class Packet:
    def __init__(self, destination, id, creationTime):
        self.destination = destination
        self.id = id
        self.creationTime = creationTime
        self.arrivalTime = -1
        self.visitedNodes = []
        self.source = ''
        self.receivedPackets = []

class Router:
    def __init__(self, id, energyLevel, immediateNeighbors):
        self.id = id
        self.energyLevel = energyLevel
        self.immediateNeighbors = immediateNeighbors
        self.pathTable = {}
        self.bufferQueue = []

    def learnPaths(self, path):
        # given a path, should add any new/updated paths to the path table
        print("UH OH! Function \"learnPaths\" not implemented!")
        for destination in reversed(path): # this should go backwards? then don't need the next line
            if destination in self.pathTable:
                # a route to this destination is already known, check if this path is shorter
                # if so, update it, otherwise, go to next
                print("hi")
            else:
                # new path known! add to dictionary
                print("hi")

    def getTopPacketAndHop(self):
        # should return two things, the next hop for the top packet and the top packet
        # the next hop should be either found by the path table
        # if the path table does not have the answer, randomly choose a neighbor
        # decrement energy when packet is sent
        print("UH OH! Function \"getTopPacketAndHop\" not implemented!")

    def receivePacket(self, newPacket, currentTime):
        # given a new packet, the router should process the packet
        # if router = destination:
            # send the packet's path to the learn paths function
            # remove packet from the sim and add to stats
        # else
            # send the packet's path to the learn paths function
            # add the packet to the bufferQueue
        self.learnPaths(newPacket.visitedNodes)
        if(newPacket.destination == self.id):
            newPacket.arrivalTime == currentTime   
            self.receivedPackets.append(newPacket) 
        else:
            self.bufferQueue.append(newPacket)


# begin of main
# read in file of nodes and connections
globalView = {}

file = open("network_one.csv", "r")
for x in file:
    x = x.split(",")
    x[-1] = x[-1].replace('\n', "")
    globalView[x[0]] = x[1:]
test = Router(1,2,3)
test.learnPaths(['a','b','c','e'])

print(globalView["a"])



