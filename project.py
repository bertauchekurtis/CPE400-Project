# kurtis bertauche
# cpe 400 project
# project.py

# libraries
import random
import sys
import copy
import statistics
RANDOM_SEED = 10
random.seed(RANDOM_SEED)

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
        self.delay = -1 # will be filled with the amount of delay when the packet arrives

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
            self.pathTables.append(dict()) # creates n dictionaries for the n shortest paths

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
            elif (isNewPathUnique == True) and (len(pathToDest) < longestStoredPath):
                self.pathTables[longestStoredPathIndex][destNode] = pathToDest

    def getTopPacket(self):
        if(len(self.bufferQueue) > 0):
            self.energyLevel -= 1
            self.bufferQueue[0].hopCount += 1
            return self.bufferQueue.pop(0)

    def getTopPacketNextHop(self):
        # if the path is known, we just return the next node in the path, otherwise, we return all of the neighbors for broadcasting
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
            if(self.id not in newPacket.pathInformation):
                self.learnPaths(newPacket.pathInformation)
            del newPacket
            return
        else:
            self.seenPackets.append(newPacket.id)

        if(newPacket.destinationRouter == self.id):
            # this is the destination router
            # create a copy of the packet to be able to track statistics of the simulation
            trackingPacket = copy.deepcopy(newPacket)
            trackingPacket.arrivalTime = currentTime + 1
            if(trackingPacket.pathInformation[-1] != self.id):
                trackingPacket.pathInformation.append(self.id)
            trackingPacket.delay = (currentTime - trackingPacket.creationTime) - trackingPacket.hopCount + 1
            self.finishedQueue.append(trackingPacket)

            # now, we deal with returns and learning paths
            if(newPacket.ROUTE_REQUEST == newPacket.PATH_KNOWN):
                print("ERROR! Packet received with ROUTE_REQUEST = PATH_KNOWN")
            else:
                pathCopy = list.copy(newPacket.pathInformation)
                if(newPacket.id < 0):
                    pathCopy.pop()
                if(self.id in pathCopy):
                    pathCopy.pop(pathCopy.index(self.id))
                self.learnPaths(pathCopy)
                newPacket.pathInformation.append(self.id)
                newPacket.arrivalTime = currentTime + 1
                if(newPacket.ROUTE_REQUEST == True):
                    returnPath = list.copy(newPacket.pathInformation)
                    returnPath.reverse()
                    returnPacket = Packet(False, True, returnPath, 0, self.id, newPacket.sourceRouter, -idcounter, currentTime + 1)
                    idcounter += 1
                    self.bufferQueue.append(returnPacket)
                    
        else:
            # this is not the destination router
            if(newPacket.ROUTE_REQUEST == newPacket.PATH_KNOWN):
                print("ERROR! Packet received with ROUTE_REQUEST == PATH_KNOWN")
            else:
                if(newPacket.PATH_KNOWN == True):
                    # first, handle learning paths
                    mutablePaths = list.copy(newPacket.pathInformation)
                    indexOfSelf = mutablePaths.index(self.id)
                    firstPart = mutablePaths[:indexOfSelf:]
                    secondPart = mutablePaths[indexOfSelf+1::]
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
                        random.seed(RANDOM_SEED)
                        chosenPath = random.choice(possiblePaths)
                        originalPath = list.copy(newPacket.pathInformation)
                        originalPath.reverse()
                        continuePath = newPacket.pathInformation + [self.id] + list.copy(chosenPath) + [newPacket.destinationRouter]
                        forReturn = list.copy(chosenPath)
                        forReturn.reverse()
                        returnPath = [newPacket.destinationRouter] + forReturn + [self.id] + originalPath
                        continuePacket = Packet(False, True, continuePath, continuePath.index(self.id), newPacket.sourceRouter, newPacket.destinationRouter, newPacket.id, newPacket.creationTime)
                        continuePacket.hopCount = newPacket.hopCount
                        self.bufferQueue.append(continuePacket)
                        returnPacket = Packet(False, True, returnPath, returnPath.index(self.id), newPacket.destinationRouter, newPacket.sourceRouter, -idcounter, currentTime)
                        self.bufferQueue.append(returnPacket)
                        del newPacket
                    else:
                        # we don't know a possible path
                        newPacket.pathInformation.append(self.id)
                        self.bufferQueue.append(newPacket)
 
    def spawnNewPacket(self, destinationRouter, currentTime, idcounter):
        
        possiblePaths = []
        self.seenPackets.append(idcounter)

        if destinationRouter in self.immediateNeighbors:
            newPath = [self.id, destinationRouter]
            newPacket = Packet(False, True, newPath, 0, self.id, destinationRouter, idcounter, currentTime)
            self.bufferQueue.append(newPacket)
            return

        for y in range(NUM_BEST_PATHS):
            if self.pathTables[y].get(destinationRouter) is not None:
                possiblePaths.append(self.pathTables[y].get(destinationRouter))

        if(len(possiblePaths) > 0):
            random.seed(RANDOM_SEED)
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
userPackets = 0
idcounter = 1
currentTime = 0

numArguments = len(sys.argv)
if(numArguments != 5):
    print("Error, incorrect number of command line arguments supplied. Proper usage:")
    print("py project.py <network file> <packet file> <n> <default energy level>")
    exit()

NETWORK_FILE = sys.argv[1]
PACKET_FILE = sys.argv[2]
DEFAULT_ENERGY_LEVEL = int(sys.argv[4])
NUM_BEST_PATHS = int(sys.argv[3])

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
networkAlive = True

while((anyBuffersHavePackets(routerList) or len(packetQueue) > 0) and networkAlive):
    
    # add any new packets to the queue
    while(len(packetQueue) > 0 and packetQueue[0][0] == currentTime):
        routerToAdd = routerMapping.get(packetQueue[0][1])
        routerList[routerToAdd].spawnNewPacket(packetQueue[0][2], currentTime, idcounter)
        idcounter += 1
        userPackets += 1
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
            packetToSend = copy.deepcopy(packet)
            routerList[mapping].receivePacket(packetToSend, currentTime, idcounter)
            idcounter += 1
        del packet
    
    # check if any routers have died
    for router in routerList:
        if(router.energyLevel < 1):
            networkAlive = False

    currentTime += 1

# sim has finished, collect stats
finishedPackets = []
remainingEnergies = []
userCount = 0
refCount = 0
totalUserDelay = 0
totalRefDelay = 0

for router in routerList:
    remainingEnergies.append(router.energyLevel)
    for packet in router.finishedQueue:
        if(packet.id > 0):
            userCount += 1
            totalUserDelay += packet.delay      
        else:
            refCount += 1
            totalRefDelay += packet.delay

averageUserDelay = totalUserDelay / userCount
averageRefDelay = totalRefDelay / refCount
averageOverallDelay = (totalRefDelay + totalUserDelay) / (userCount + refCount)

# Display results

print("|===== Simulation has Ended =====")
if(networkAlive):
    print("| The simulation has ended due to all packets reaching their destinations.")
else:
    print("| The simulation has ended as a router has depleted all of its energy.")
print("|================================")

print("\n|==== Packet Information ====")
print("| A total of " + str(userPackets) + " packets were loaded")
print("| Of those " + str(userPackets) + " packets, " + str(userCount) + " reached their destination [" + str((userCount/userPackets)*100) + "%]")
print("|\n| There were a total of " + str(refCount) + " additional packets for fulfilling route requests")
print("|\n| The average delay for user created packets was " + str(averageUserDelay))
print("| The average delay for route reponse packets was " + str(averageRefDelay))
print("| The overall average delay was " + str(averageOverallDelay))
print("|============================")

print("\n|==== Energy Levels ====")
print("|All routers had an initial energy level of " + str(DEFAULT_ENERGY_LEVEL))
print("|The average remaining energy level is " + str(sum(remainingEnergies)/len(routerList)))
print("|The highest remaining energy level is " + str(max(remainingEnergies)))
print("|The lowest remaining energy level is " + str(min(remainingEnergies)))
print("|The median remaining energy level is " + str(statistics.median(remainingEnergies)))
print("|The variance of remaining energy levels is " + str(statistics.variance(remainingEnergies)))
print("|=======================")