import time
class Packet(object):
    def __init__(self, id=None, size=None, rotation=None, flowId=None, targetNode=None, currentNode=None):
	self.id = id
	self.size = size
	self.rotation = rotation 
	self.flowId = flowId 
	self.targetNode = targetNode 
	self.currentNode = currentNode



class Node(object):
    def __init__(self):
        self.id = None
        self.isBusy = False
        self.queue = []
        self.rightLinkDataRate = None
	self.leftLinkDataRate = None



class Calculations(object):

    # transmissionDelay() simply calculates transmission delay by dividing packet size to data rate.
    def transmissionDelay(self, packetSize, dataRate):
	return round((float(packetSize)/dataRate),3)
    
    # shortestPath() calculates the shortest path between source node and target node.
    # This function returns a string "left" or "right" in order to indicate which way
    # the packet should go according to reach to the target node in shorter time. 
    def shortestPath(self, nodeList, sourceNode, targetNode):
	rightCounter = 0
	leftCounter = 0
	if (sourceNode < targetNode):
	    rightCounter = targetNode - sourceNode
	    leftCounter = ((len(nodeList)-1) - targetNode) + sourceNode
	    if leftCounter > rightCounter:
		return "right"
	    else:
		return "left"
	else:
	    leftCounter = sourceNode - targetNode
	    rightCounter = ((len(nodeList)-1) - sourceNode) + targetNode
	    if leftCounter > rightCounter:
	        return "right"
	    else:
	        return "left"

    # The method below takes a packet as an argument and then returns the node
    # that the packet should go next.
    def findNextNode(self, nodeList, packet):
        if packet.rotation == "right":
	    if nodeList[(packet.currentNode+1)%len(nodeList)] == None:
	        return nodeList[(packet.currentNode+2)%len(nodeList)].id
	    else:
	        return nodeList[(packet.currentNode+1)%len(nodeList)].id
	elif packet.rotation == "left":
	    if nodeList[(packet.currentNode-1)%len(nodeList)] == None:
                return nodeList[(packet.currentNode-2)%len(nodeList)].id
	    else:
		return nodeList[(packet.currentNode-1)%len(nodeList)].id


    transmissionDelayByRoute = lambda packet, nodeList: self.transmissionDelay(packet.size, nodeList[packet.currentNode].rightLinkDataRate) if packet.rotation == "right" else (self.transmissionDelay(packet.size, nodeList[packet.currentNode].leftLinkDataRate)) 
    def transmissionDelayByRoute2(self, packet, nodeList):
        if packet.rotation == "right":
	    return self.transmissionDelay(packet.size, nodeList[packet.currentNode].rightLinkDataRate)
        else:
	    return self.transmissionDelay(packet.size, nodeList[packet.currentNode].leftLinkDataRate)

class Network(object):

    def __init__(self):
        # Initialize default attributes.
	self.clock = 0.0
	self.linkList = [None]
        self.nodeList = [None]
        self.nodeNum = input('Enter the number of nodes in the network: ')
        self.defaultDataRate = input('Enter the data rate of each link (Mb/s): ')
        self.propogationDelay = (input('Enter the propogation delay of each link (microsec): '))/1000.0 #Convert to millisecond.

        # Get the bottleneck properties.
        self.bottleNecks = [None] #[(link x,dataRate x),(link y,dataRate y ),...]
        self.bottleneckNum = input('Enter the number of bottlenecks: ')
        for n in range(1, self.bottleneckNum+1):
           self.bottleNecks.append(input('Enter bottleneck link %d and its data rate: '%n))

        # Get flow properties of the network.
        self.flowProperties  = [None] # A list to hold properties of each flow.
        self.flowNum = input('Enter the number of flows in the network: ')
        for n in range(1, self.flowNum+1):
            self.flowProperties.append(input('Enter data flow %d (source, destination, message size, packet #): ' %n))

	self.calculations = Calculations()
        self.createNetwork()


    def createNetwork(self):
        # This method creates nodes and links, then initialize their attributes.

	for i in range(1,self.nodeNum+1):
	    self.linkList.append(self.defaultDataRate) # Assign the default data rate to all links.

	for bottleNeck in self.bottleNecks:
            if bottleNeck is None:
                pass
            else:
                self.linkList[bottleNeck[0]] = bottleNeck[1] # This part assigns data rate of bottleneck links.

    
	# This chunk of code create nodes and initializes their attributes.
        for i in range(1,(self.nodeNum+1)):
            self.nodeList.append(Node())
            self.nodeList[i].id = i
            self.nodeList[i].rightLinkDataRate = self.linkList[i]
	    # This part exist for avoidance of assigning None to leftLinkDataRate of the first Node.
	    if self.linkList[i-1] != None:
	        self.nodeList[i].leftLinkDataRate = self.linkList[i-1]
	    else:
	    	self.nodeList[i].leftLinkDataRate = self.linkList[-1]

	    
	currentFlowId = 1
        self.packetList = [None]
	for flow in self.flowProperties:
	    if flow != None:
		packetSize = round((float(flow[2])/flow[3]),3) # (message size)/(packet number)
		rot = self.calculations.shortestPath(nodeList=self.nodeList, sourceNode=flow[0], targetNode=flow[1])
		self.packetList.append([Packet(id=i, rotation=rot, size=packetSize, currentNode=flow[0], targetNode=flow[1], flowId=currentFlowId) for i in xrange(1,flow[3]+1)])
                # currentFlowId below here used as an index to add None front of each flow to maintain lists better. 
		# (Index 0 is always None in this project.)
		self.packetList[currentFlowId].insert(0,None) 
                currentFlowId = currentFlowId + 1
	    else:
	        continue

	# THIS PART CONTAINS SOME USEFUL FUNCTIONS THAT USED WHEN INITIALIZING FEL!!!
	
	# Initialization of the Future Event List    
	self.FEL = []	
	for flow in self.packetList:
	    if flow != None:
		for packet in flow:
		    if packet != None:
		        if packet.id == 1:
		            self.FEL.append({
			     	        "Event":"Departure", 
				        "Time": self.clock + self.calculations.transmissionDelayByRoute2(packet, self.nodeList), 
				        "From/To": packet.currentNode,
				        "PacketID":packet.id, 
				        "FlowID":packet.flowId
				        })
			    continue		
			self.nodeList[packet.currentNode].queue.append(packet) # This line adds the packet to queue of convenient node.
		    else:
	    	        continue
	    else:
	        continue

    def simulate(self):
	while(len(self.FEL) != 0):
	    time.sleep(2)
	    self.FEL = sorted(self.FEL, key=lambda k: (k["Time"],k["FlowID"])) # Sorts the FEL by Time then FlowID in ascending order.

	    currentEvent = self.FEL[0] 
	    del self.FEL[0] # This line removes the current event from the FEL.
            
	    self.clock = currentEvent["Time"] 
            event = currentEvent["Event"]
	    # ARRIVAL SCENARIO
	    if event  == "Arrival":
	        print "(Flow{}) Packet{} arrived to Node{} at time {} ms.".format(currentEvent["FlowID"], currentEvent["PacketID"], currentEvent["From/To"], currentEvent["Time"])
		print "-----------------------------------------------------"
	        if self.nodeList[currentEvent["From/To"]].isBusy == False:
	            self.nodeList[currentEvent["From/To"]].isBusy = True # Set isBusy flag of current the  node True.
	            currentEvent["Event"] = "Departure"
		    currentEvent["Time"] = currentEvent["Time"] + self.calculations.transmissionDelayByRoute2(self.packetList[currentEvent["FlowID"]][currentEvent["PacketID"]], self.nodeList)
		    if self.packetList[currentEvent["FlowID"]][currentEvent["PacketID"]].targetNode != currentEvent["From/To"]:
		        self.FEL.append(currentEvent)
                else:
	            self.nodeList[currentEvent["From/To"]].queue.append(self.packetList[currentEvent["FlowID"]][currentEvent["PacketID"]])

	    
	    # DEPARTURE SCENARIO
	    if event  == "Departure":
		temporaryNodeIndex = currentEvent["From/To"]
		print "(Flow{}) Packet{} departed from Node{} at time {} ms.".format(currentEvent["FlowID"], currentEvent["PacketID"], currentEvent["From/To"], currentEvent["Time"])
		print "-----------------------------------------------------"
		currentEvent["Event"] = "Arrival"
		currentEvent["Time"] = currentEvent["Time"] + self.propogationDelay
		currentEvent["From/To"] = self.calculations.findNextNode(self.nodeList, self.packetList[currentEvent["FlowID"]][currentEvent["PacketID"]])
		self.packetList[currentEvent["FlowID"]][currentEvent["PacketID"]].currentNode = currentEvent["From/To"]
                self.FEL.append(currentEvent)
	        if len(self.nodeList[temporaryNodeIndex].queue) > 0:
	            # self.nodeList[currentEvent["From/To"]].queue.remove(self.packetList[currentEvent["FlowID"]][currentEvent["PacketID"]])
		    nextPacketInTheQueue = self.nodeList[temporaryNodeIndex].queue[0]
		    del self.nodeList[temporaryNodeIndex].queue[0]
                    eventTemplate = {
		            "Event": "Departure",
			    "Time": self.clock + self.calculations.transmissionDelayByRoute2(nextPacketInTheQueue, self.nodeList),
			    "From/To": nextPacketInTheQueue.currentNode,
			    "FlowID": nextPacketInTheQueue.flowId,
			    "PacketID": nextPacketInTheQueue.id
		            }
		    self.FEL.append(eventTemplate)	    
		else:
		    self.nodeList[temporaryNodeIndex].isBusy = False
