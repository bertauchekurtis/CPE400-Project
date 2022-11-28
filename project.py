# kurtis bertauche
# cpe 400 project
# project.py

# libraries
NUM_BEST_PATHS = 3

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

        for x in range(NUM_BEST_PATHS):
            self.pathTables.append(dict())

    def learnPaths(self, path):
        mutablePathList = list.copy(path)
        for x in range(len(mutablePathList) - 1):
            # determine all of the paths
            destNode = mutablePathList.pop(0)
            pathToDest = list.copy(mutablePathList)
            list.reverse(pathToDest)

            # print for debug:
            # print("Path to node: " + destNode, end = " ")
            # for y in range(len(pathToDest)):
            #   print(pathToDest[y], end = ", ")
            # print("\n")

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
                #print("New path is unique") # debug
            elif (isNewPathUnique == True) and (len(thisPath) < longestStoredPath):
                self.pathTables[longestStoredPathIndex][destNode] = pathToDest
                #print("New path is unique and shorter") # debug
            else:
                #print("New path is not shorter or unique, not stored") # debug
            

    def getTopPacketAndHop(self):
        print("UH OH! Function \"getTopPacketAndHop\" not implemented!")

    def receivePacket(self, newPacket, currentTime):
        print("UH OH")


# begin of main
# read in file of nodes and connections
globalView = {}

file = open("network_one.csv", "r")
for x in file:
    x = x.split(",")
    x[-1] = x[-1].replace('\n', "")
    globalView[x[0]] = x[1:]
test = Router(1,2,3)
test.learnPaths(['a','b','c','d'])
test.learnPaths(['a','b','c','d'])
test.learnPaths(['a','e','c','d'])
test.learnPaths(['a','f','c','d'])
test.learnPaths(['a','j','c','d'])
pack = Packet(True, True, 1, 2, 3, 4, 5, 6)

print(globalView["a"])



