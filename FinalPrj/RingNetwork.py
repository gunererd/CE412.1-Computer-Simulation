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
	dummyFunc = lambda x: self.calculations.transmissionDelay(x.size, self.nodeList[x.currentNode].rightLinkDataRate) if x.rotation == "right" else (self.calculations.transmissionDelay(x.size, self.nodeList[x.currentNode].leftLinkDataRate)) 
	def dummyFunc2(packet):
	    if packet.rotation == "right":
		if self.nodeList[(packet.currentNode+1)%len(self.nodeList)] == None:
		    return self.nodeList[(packet.currentNode+2)%len(self.nodeList)].id
		else:
		    return self.nodeList[(packet.currentNode+1)%len(self.nodeList)].id
	    elif packet.rotation == "left":
		if self.nodeList[(packet.currentNode-1)%len(self.nodeList)] == None:
		    return self.nodeList[(packet.currentNode-2)%len(self.nodeList)].id
		else:
		    return self.nodeList[(packet.currentNode-1)%len(self.nodeList)].id

	# Initialization of the Future Event List    
	self.FEL = []	
	for flow in self.packetList:
	    if flow != None:
		for packet in flow:
		    if packet != None:
		        self.FEL.append({
				    "Event":"Departure", 
				    "Time": self.clock + packet.id * dummyFunc(packet), 
				    "From/To": paket.currentNode
				    "PacketID":packet.id, 
				    "FlowID":packet.flowId
				    })
			self.nodeList[packet.currentNode].queue.append(packet) # This line adds the packet to queue of convenient node.
		    else:
	    	        continue
	    else:
	        continue

    def simulate(self):
	while(len(self.FEL != 0)):
	    self.FEL = sorted(self.FEL, key=lambda k: (k["Time"],k["FlowID"])) # Sorts the FEL by Time then FlowID in ascending order.

	    currentEvent = self.FEL[0] 
	   
	    # ARRIVAL SCENARIO
	    if currentEvent["Event"] == "Arrival":
	        if self.nodeList[currentEvent["From/To"]].isBusy == False:
	            self.nodeList[currentEvent["From/To"]].isBusy = True # Set isBusy flag of current node True.
	            currentEvent.["Event"] = "Departure"
		    currentEvent.["Time"] = currentEvent["Time"] + dummyFunc(self.packetList[currentEvent["FlowID"]][currentEvent["PacketID"]])
		    self.FEL[0] = currentEvent
                else:
	            self.nodeList[currentEvent["From/To"]].queue.append(self.packetList[currentEvent["FlowID"]][currentEvent["PacketID"]])

	    
	    # DEPARTURE SCENARIO
	    if currentEvent["Event"] == "Departure":
	        if len(self.nodeList[currentEvent["From/To"]].queue) > 0:
	            self.nodeList[currentEvent["From/To"]].queue.remove(self.packetList[currentEven["FlowID"]][currentEven["PacketID"]])
                    currentEvent["Event"] = "Arrival"
		    currentEvent["Time"] = currentEvent["Time"] + self.propogationDelay
