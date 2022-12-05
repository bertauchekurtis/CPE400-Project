# kurtis bertauche
# cpe 400 project
# project.py

# libraries
NUM_BEST_PATHS = 3
DEFAULT_ENERGY_LEVEL = 5
NETWORK_FILE = "network_one.csv"
PACKET_FILE = "packets.csv"
import random
import sys

class Packet:
    def __init__(self, ROUTE_REQUEST, PATH_KNOWN, pathInformation, placeInPath, sourceRouter, destinationRouter, id, creationTime):
        self.ROUTE_REQUEST = ROUTE_REQUEST
        self.PATH_KNOWN = PATH_KNOWN
        self.pathInformation = pathInformation
        self.placeInPath = placeInPath
        self.sourceRouter = sourceRouter
        self.destinationRouter = destinationRouter
        self.id = id
        self.creationTime = creationTime
        self.arrivalTime = -1 # indicates the packet has not arrived yet
        self.hopCount = 0

        # now, do some error checking
        if(self.ROUTE_REQUEST == self.PATH_KNOWN):
            print("ERROR! ==================================\nAttempt to set ROUTE_REQUEST equivalent to PATH_KNOWN in packet: " + str(id))
            print("=========================================") 


class Router:
    def __init__(self, id, energyLevel, immediateNeighbors):
        self.id = id
        self.energyLevel = energyLevel
        self.immediateNeighbors = immediateNeighbors
        self.pathTables = []
        self.bufferQueue = []
        self.finishedQueue = []
        self.seenPackets = []

        for x in range(NUM_BEST_PATHS):
            self.pathTables.append(dict())

    def learnPaths(self, path):
        mutablePathList = list.copy(path)
        for x in range(len(mutablePathList) - 1):
            # determine all of the paths
            destNode = mutablePathList.pop(0)
            pathToDest = list.copy(mutablePathList)
            list.reverse(pathToDest)

            # now, destNode holds the node for the path in pathToDest
            isNewPathUnique = True
            emptyPathTableIndex = -1
            longestStoredPath = -1
            longestStoredPathIndex = -1
            # get all of the current stored paths to that destNode
            # this goes through all of the current stored paths
            # at the end of this loop the following will be known:
            #   isNewPathUnique will tell if the newPath is unique or already stored in the tables
            #   longestStoredPath will tell the longest path that is currently stored (-1 if no paths stored)
            #   emptyPathTableIndex will hold the index of the table that doesn't have a path (if there is one)
            #   longestStoredPathIndex will tell where the index of the longest path is
            for y in range(NUM_BEST_PATHS):
                if self.pathTables[y].get(destNode) is not None:
                    thisPath = self.pathTables[y].get(destNode)
                    if len(thisPath) > longestStoredPath:
                        longestStoredPath = len(thisPath)
                        longestStoredPathIndex = y
                    if thisPath == pathToDest:
                        isNewPathUnique = False
                else:
                    emptyPathTableIndex = y

            # if the path is unique and there is an empty table, we store it
            # if the path is unique and there is not an empty table, we store it if it is shorter than one of the current paths
            # otherwise, we don't store it
            if (isNewPathUnique == True) and (emptyPathTableIndex != -1):
                self.pathTables[emptyPathTableIndex][destNode] = pathToDest
            elif (isNewPathUnique == True) and (len(thisPath) < longestStoredPath):
                self.pathTables[longestStoredPathIndex][destNode] = pathToDest
            

    def getTopPacket(self):
        if(len(self.bufferQueue) > 0):
            self.energyLevel -= 1
            self.bufferQueue[0].hopCount += 1
            return self.bufferQueue.pop(0)


    def getTopPacketNextHop(self):
        if(len(self.bufferQueue) > 0):
            topPacket = self.bufferQueue[0]
            if(topPacket.PATH_KNOWN == True):
                topPacket.placeInPath += 1
                return [topPacket.pathInformation[topPacket.placeInPath]]
            else:
                return list.copy(self.immediateNeighbors)


    def receivePacket(self, newPacket, currentTime, idcounter):
        # determine if this is the detination
        if(newPacket.id in self.seenPackets):
            # already saw this packet
            return
        else:
            self.seenPackets.append(newPacket.id)

        if(newPacket.destinationRouter == self.id):
            # this is the destination router
            if(newPacket.ROUTE_REQUEST == newPacket.PATH_KNOWN):
                print("ERROR! Packet received with ROUTE_REQUEST = PATH_KNOWN")
            else:
                self.learnPaths(newPacket.pathInformation)
                newPacket.pathInformation.append(self.id)
                newPacket.arrivalTime = currentTime + 1
                if(newPacket.ROUTE_REQUEST == True):
                    returnPath = list.copy(newPacket.pathInformation)
                    returnPath.reverse()
                    returnPacket = Packet(False, True, returnPath, 0, self.id, newPacket.sourceRouter, -idcounter, currentTime + 1)
                    idcounter += 1
                    self.bufferQueue.append(returnPacket)
                    self.finishedQueue.append(newPacket)
                else:
                    self.finishedQueue.append(newPacket)
                    
        else:
            # this is not the destination router
            if(newPacket.ROUTE_REQUEST == newPacket.PATH_KNOWN):
                print("ERROR! Packet received with ROUTE_REQUEST == PATH_KNOWN")
            else:
                if(newPacket.PATH_KNOWN == True):
                    # first, handle learning paths
                    mutablePaths = list.copy(newPacket.pathInformation)
                    midpoint = newPacket.placeInPath
                    firstPart = mutablePaths[:midpoint+1]
                    secondPart = mutablePaths[midpoint+2:]
                    secondPart.reverse()
                    self.learnPaths(firstPart)
                    self.learnPaths(secondPart)
                    # now we can pass it along
                    self.bufferQueue.append(newPacket)

                else:
                    mutablePaths = list.copy(newPacket.pathInformation)
                    self.learnPaths(mutablePaths)
                    # need to do a few things
                    # first, see if we know a path to this packet's destionation
                    # if so, give the packet that path and send it on its way
                    # and also give a response packet back to source with the full path
                    # otherwise, forward to everyone
                    targetDestination = newPacket.destinationRouter
                    possiblePaths = []
                    for y in range(NUM_BEST_PATHS):
                        if self.pathTables[y].get(targetDestination) is not None:
                            possiblePaths.append(self.pathTables[y].get(targetDestination))
                    if(len(possiblePaths) > 0):
                        # we know a possible path
                        chosenPath = random.choice(possiblePaths)
                        returnPath = list.copy(chosenPath)
                        returnPath.reverse()
                        returnPath.insert(0, newPacket.destinationRouter)
                        num = len(returnPath)
                        returnPath.append(self.id)
                        otherPart = list.copy(newPacket.pathInformation)
                        otherPart.reverse()
                        returnPath = returnPath + otherPart
                        newPacket.pathInformation = chosenPath
                        newPacket.pathInformation.append(newPacket.destinationRouter)
                        newPacket.pathInformation.insert(0, self.id)
                        newPacket.placeInPath = 0
                        newPacket.PATH_KNOWN = True
                        newPacket.ROUTE_REQUEST = False
                        self.bufferQueue.append(newPacket)
                        # now send the return packet
                        returnPacket = Packet(False, True, returnPath, num, self.id, newPacket.sourceRouter, -idcounter, currentTime)
                        self.bufferQueue.append(returnPacket)
                        
                    else:
                        # we don't know a possible path
                        newPacket.pathInformation.append(self.id)
                        self.bufferQueue.append(newPacket)
                    
                    
                    

    def spawnNewPacket(self, destinationRouter, currentTime, idcounter):
        
        possiblePaths = []
        self.seenPackets.append(idcounter)

        for y in range(NUM_BEST_PATHS):
            if self.pathTables[y].get(destinationRouter) is not None:
                possiblePaths.append(self.pathTables[y].get(destinationRouter))

        if(len(possiblePaths) > 0):
            chosenPath = random.choice(possiblePaths)
            mutable = list.copy(chosenPath)
            mutable.append(destinationRouter)
            mutable.insert(0, self.id)
            newPacket = Packet(False, True, mutable, 0, self.id, destinationRouter, idcounter, currentTime)
            self.bufferQueue.append(newPacket)
        else:
            newPacket = Packet(True, False, [self.id], 0, self.id, destinationRouter, idcounter, currentTime)
            self.bufferQueue.append(newPacket)

def anyBuffersHavePackets(routerList):
    for x in routerList:
        if(len(x.bufferQueue) > 0):
            return True
    return False
            

# begin of main
# read in file of nodes and connections
routerList = []
routerMapping = {}
packetQueue = []
statTrackList = []
idcounter = 0
currentTime = 0

file = open(NETWORK_FILE, "r")

for x in file:
    x = x.split(",")
    x[-1] = x[-1].replace('\n', "")
    neighbors = list.copy(x[1:])
    newRouter = Router(x[0], DEFAULT_ENERGY_LEVEL, neighbors)
    routerList.append(newRouter)
    routerMapping[x[0]] = len(routerList) - 1

pfile = open(PACKET_FILE, "r")

for x in pfile:
    x = x.split(",")
    x[-1] = x[-1].replace('\n', "")
    packetQueue.append([int(x[0]), x[1], x[2]])

packetQueue.sort(key=lambda x: x[0])
userNumPackets = len(packetQueue)
networkAlive = True

while((anyBuffersHavePackets(routerList) or len(packetQueue) > 0) and networkAlive):
    
    # add any new packets to the queue
    while(len(packetQueue) > 0 and packetQueue[0][0] == currentTime):
        routerToAdd = routerMapping.get(packetQueue[0][1])
        routerList[routerToAdd].spawnNewPacket(packetQueue[0][2], currentTime, idcounter)
        statTrackList.append(idcounter)
        idcounter += 1
        packetQueue.pop(0)
    
    # make a list of all the routers that have something to process
    routersToProcess = []
    for router in routerList:
        if(len(router.bufferQueue) > 0):
            routersToProcess.append(routerMapping.get(router.id))

    # let those routers process
    for routerIndex in routersToProcess:
        listToSend = routerList[routerIndex].getTopPacketNextHop()
        packet = routerList[routerIndex].getTopPacket()
        for nextHop in listToSend:
            mapping = routerMapping.get(nextHop)
            routerList[mapping].receivePacket(packet, currentTime, idcounter)
            idcounter += 1
    
    # check if any routers have died
    for router in routerList:
        if(router.energyLevel < 1):
            networkAlive = False

    currentTime += 1

# sim has finished, collect stats
finishedPackets = []
remainingEnergies = []
for router in routerList:
    finishedPackets = finishedPackets + router.finishedQueue
    remainingEnergies.append(router.energyLevel)

avgDelay = 0
statAvgDelay = 0

for packet in finishedPackets:
    avgDelay += (packet.arrivalTime - packet.creationTime - packet.hopCount)
    if(packet.id >= 0):
        statTrackList.remove(packet.id)
        statAvgDelay += (packet.arrivalTime - packet.creationTime - packet.hopCount)

print("===== Simulation has Ended =====")
if(networkAlive):
    print("The simulation has ended due to all packets reaching their destinations.")
else:
    print("The simulation has ended as a router has depleted all of its energy.")
print("\n===== Summary of Simulation =====")
print("A total of " + str(userNumPackets) + " packet(s) were loaded into the simulation.")
print("Of those " + str(userNumPackets) + " packets, " + str(userNumPackets - len(statTrackList)) + " reached their destination [" + str((userNumPackets/(userNumPackets-len(statTrackList)))*100) + " %]")
if(userNumPackets == len(statTrackList)):
    print("An average delay for these packets cannot be calculated as none of them reached their destination")
else:
    print("The average delay was " + str(statAvgDelay/(userNumPackets - len(statTrackList))))
    print("The delay indicates any time that a packet was waiting in a buffer due to other packets already at that router needing to be sent.")
print("\n===== Overall Network =====")
if(len(finishedPackets) == 0):
    print("The overall network statistics cannot be calculated as no packets (route reponses or requested transmissions) were received.")
else:
    print("The total number of packets received (route reponses + requested transmissions) was " + str(len(finishedPackets)) + ".")
    print("Out of all packets (route reponses + requested transmissions), the average delay was " + str(avgDelay/len(finishedPackets)))
print("\n==== Energy Levels ====")
print("All routers had an initial energy level of " + str(DEFAULT_ENERGY_LEVEL))
print("The average remaining energy level is " + str(sum(remainingEnergies)/len(routerList)))
print("The highest remaining energy level is " + str(max(remainingEnergies)))
print("The lowest remaining energy level is " + str(min(remainingEnergies)))




