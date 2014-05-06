class Packet:

	def __init__(self,id,targetNode,currentNode):
		self.id = id
		self.time = 0



class Network:


	''' Represent a network '''

	def __init__(self):
		
		self.nodeNum = input('Enter number of nodes:\t')
		self.dataRate = input('Enter data rate of links in Mbps:\t')
		self.propDelay = float(input('Enter propogation delay of a link in microsecond:\t'))/1000
		self.sender = input('Sender node:\t')
		self.target = (input('Target node:\t'))%self.nodeNum
		self.totalSize = input('Total size of the message in Mb:\t')
		self.numberOfPackets = input('The number of packets that the message will be divided into:\t')
		#self.time = 0
		self.createNetwork()
		self.receivedPacketList = []
		




	def createNetwork(self):

		self.nodeList = [("Node"+str(n)) for n in xrange(self.nodeNum)] 


		''' This part calculates transmission delay for each node. '''

		self.packetSize = float(self.totalSize)/float(self.numberOfPackets)
		self.transmissionDelay = float(self.packetSize)/float(self.dataRate)

		''' Creates a list of packets '''
		
		self.packetList = [Packet(("Packet" + str(id)),self.nodeList[self.target],self.nodeList[self.sender]) for id in xrange(1,self.numberOfPackets+1)] 
		for i in range(1,len(self.packetList)):
			self.packetList[i].time = self.packetList[i].time + self.transmissionDelay*i






	def shortestPath(self):
		
		''' Calculates shortest path from left and right. Returns "Left" or "Right" string. '''

		self.dummy = self.sender
		
		self.counterL = 0
		self.counterR = 0

		while(self.nodeList[self.dummy] != self.nodeList[self.target]):
			self.counterR = self.counterR + 1
			self.dummy = self.dummy + 1
		
		self.dummy = self.sender
		
		while(self.nodeList[self.dummy] != self.nodeList[self.target]):
			self.counterL = self.counterL + 1
			self.dummy = self.dummy - 1

		if min(self.counterR,self.counterL) == self.counterR:
			return "Right"
		else:
			return "Left"	

	

	def monitorPackets(self):

		if self.shortestPath() == "Right":
			self.counter = self.sender
			while(True):
				for i in self.packetList:
					i.time = i.time + self.transmissionDelay
					print "At second {}, {} transmitted from {}. ".format(i.time,i.id,self.nodeList[self.counter%self.nodeNum])
					i.time = i.time + self.propDelay
					print "At second {}, {} arrived to {}.\n ".format(i.time,i.id,self.nodeList[(self.counter+1)%self.nodeNum])
					if self.nodeList[(self.counter+1)%self.nodeNum] == self.nodeList[self.target]:
						print "{} RECEIVED BY TARGET!\n".format(i.id)
						self.receivedPacketList.append(i)
					if len(self.receivedPacketList) == self.numberOfPackets:
						return	
				self.counter = self.counter + 1	
		

		else:
			self.counter = self.sender
			while(True):
				for i in self.packetList:
					i.time = i.time + self.transmissionDelay
					print "At second {}, {} transmitted from {}. ".format(i.time,i.id,self.nodeList[self.counter])
					i.time = i.time + self.propDelay
					print "At second {}, {} arrived to {}.\n ".format(i.time,i.id,self.nodeList[self.counter-1])
					if self.nodeList[self.counter-1] == self.nodeList[self.target]:
						print "{} RECEIVED BY TARGET!\n".format(i.id)
						self.receivedPacketList.append(i)
					if len(self.receivedPacketList) == self.numberOfPackets:
						return	
				self.counter = self.counter - 1	






