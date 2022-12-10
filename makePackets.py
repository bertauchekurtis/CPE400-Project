# kurtis bertauche
# CPE 400 project
# makePackets.py

import random
import sys

numArguments = len(sys.argv)
if(numArguments != 5):
    print("Error, incorrect number of command line arguments supplied. Proper usage:")
    print("py makePackets.py <network file> <number of packts> <max spawn time> <output file>")
    exit()

NETWORK_FILE = sys.argv[1]
NUM_PACKETS = int(sys.argv[2])
MAX_SPAWN_TIME = int(sys.argv[3])
OUT_FILE = sys.argv[4]

networkFile = open(NETWORK_FILE, "r")
routerList = []

for router in networkFile:
    router = router.split(",")
    routerList.append(router[0])

packetFile = open(OUT_FILE, "w")

for i in range(1, NUM_PACKETS + 1):
    sourceRouter = random.choice(routerList)
    destinationRouter = random.choice(routerList)
    spawnTime = random.randint(0, MAX_SPAWN_TIME)
    while(sourceRouter == destinationRouter):
        sourceRouter = random.choice(routerList)

    packetFile.write(str(spawnTime) + "," + sourceRouter + "," + destinationRouter + "\n")

packetFile.close()