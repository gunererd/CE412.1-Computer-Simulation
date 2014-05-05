import random


''' A function to observe behaviour of random.expovariate()'''
def deneme(liste, loop, lambd):
	del liste[:]
	for i in range(loop):
		liste.append(random.expovariate(lambd))
	return round(sum(liste)/len(liste),4)	



''' Server class.'''
class Server(object):

	''' Initialization of various attributes.'''
	def __init__(self):
		self.avg_arrival_rate = float(input('Enter average arrival rate:\t'))
		self.avg_service_rate = float(input('Enter average service rate:\t'))
		self.capacity_of_queue = input('Enter capacity of the system (<=0 for infinite):\t')
		self.clock = 0
		self.end_time = input('Simulation will be interrupted at CLOCK:\t')
		
		'''Initial value of FEL["Departure"] set higher than 
		FEL["Arrival"] to make arrival the first event.'''
		self.FEL = {"Arrival":0, "Departure":"------"} 
		
		self.isServerBusy = False
		self.nPackets_in_queue = 0
		self.loss_packet_num = 0

		self.total_packet_num = 0
		self.total_packet_num_queue = 0
		self.total_service_time = 0
		self.total_serviced = 0
		self.total_snap_number = 0
    

	def genArrival(self):
		self.FEL["Arrival"] = round(self.clock+(random.expovariate(self.avg_arrival_rate)),3)


	
	def genDeparture(self):
		
		self.service_time = random.expovariate(self.avg_service_rate)

		self.total_service_time += self.service_time

		self.FEL["Departure"] = round(self.clock+(self.service_time),3)	



			
	def simulate(self):		

		while(True):
			

			current_event = min(self.FEL, key=self.FEL.get)
			

			self.old_clock = self.clock
			self.clock = self.FEL[current_event]
			if self.clock > self.end_time:
				break


			'''Arrival Scenario'''
			if current_event == "Arrival":

				if self.isServerBusy == False:
					self.isServerBusy = True
					self.genDeparture() # For current packet
					self.genArrival() # For next packet 
					

				else:
					if self.capacity_of_queue <= 0:
						self.nPackets_in_queue += 1
					else:
						if self.nPackets_in_queue < self.capacity_of_queue:
							self.nPackets_in_queue += 1
						else:
							self.loss_packet_num += 1	
					self.genArrival()
				
				

				# Collect Statistics
				
				

			'''Departure Scenario'''
			if current_event == "Departure":
				if self.nPackets_in_queue > 0:
					self.nPackets_in_queue -= 1
					self.genDeparture()
					self.total_serviced += 1
					

				else:
					self.isServerBusy = False
					self.FEL["Departure"] = "------"
					self.total_serviced += 1
					
				# Collect Statistics	
			
			
				
			self.total_packet_num += (self.nPackets_in_queue) + (self.isServerBusy)

			self.total_packet_num_queue += (self.nPackets_in_queue)

			print "CLOCK: {}         LS(t): {}          LQ(t): {}         A({})   D({})      Queue: {}     Loss: {}\n   ".format(self.clock, self.isServerBusy, self.nPackets_in_queue != 0, self.FEL["Arrival"], self.FEL["Departure"], self.nPackets_in_queue, self.loss_packet_num)

			self.total_snap_number += 1
	
	def stats(self):
		print "---------------------------------------------------------------------------------"
		self.avg_packet_system = float(self.total_packet_num)/self.total_snap_number
		print "The average number of packets in the system = {}.\n".format(self.avg_packet_system)

		self.avg_packet_queue = float(self.total_packet_num_queue)/self.total_snap_number
		print "The average number of packets in the queue = {}.\n".format(self.avg_packet_queue)

		self.avg_waiting_time_system = (float(self.total_service_time)/self.total_serviced)*self.avg_packet_system
		print "The average waiting time in the system = {} unit.\n".format(self.avg_waiting_time_system)

		self.avg_waiting_time_queue = (float(self.total_service_time)/self.total_serviced)*self.avg_packet_queue
		print "The average waiting time in the queue = {} unit.\n".format(self.avg_waiting_time_queue) 

		self.loss_ratio = (float(self.loss_packet_num)/(self.total_packet_num + self.loss_packet_num))*100
		print "The loss ratio = {}.".format(self.loss_ratio)
		print "---------------------------------------------------------------------------------"
