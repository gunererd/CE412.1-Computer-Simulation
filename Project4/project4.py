import random

class Corporation(object):

	def __init__(self):
		self.max_car_num = float(input('Enter maximum car number: \t'))
		self.clock = 0
		self.w_service_distro = [8,8,8,10,10,10,10,12,12,12]
		random.shuffle(self.w_service_distro)
		self.d_service_distro = [5,5,8,8,8,10,10,10,10,10]
		random.shuffle(self.d_service_distro)
		self.arrived_car_num = 0
		self.FEL = {"WashArr":0, "WashDep":"---", "DryArr":"---", "DryDep":"---"}
		self.isWasherBusy = False
		self.isDrierBusy = False
		self.washerQ = 0
		self.dryerQ = 0
		self.wServiceTime = 0
		self.wServiceTime_TOTAL = 0
		self.dServiceTime = 0
		self.dServiceTime_TOTAL = 0
		self.total_serviced_D = 0
		self.total_serviced_W = 0
		self.avg_time_in_sys = 0
		self.avg_time_service_D = 0
		self.avg_time_service_W = 0



	def wGenArrival(self):
		self.FEL["WashArr"] = (self.clock + (random.randint(5,15)))
		self.arrived_car_num += 1

	def wGenDeparture(self):
		self.wServiceTime = float((random.choice(self.w_service_distro)))
		self.wServiceTime_TOTAL += self.wServiceTime
		self.FEL["WashDep"] = (self.clock + self.wServiceTime) 
		
	def dGenDeparture(self):
		self.dServiceTime = float((random.choice(self.w_service_distro)))   	
		self.dServiceTime_TOTAL += self.dServiceTime
		self.FEL["DryDep"] = (self.clock + self.dServiceTime) 




	def simulate(self):
		while(True):
			current_event = min(self.FEL, key=self.FEL.get)

			self.old_clock = self.clock
			self.clock = self.FEL[current_event]
			if self.arrived_car_num > self.max_car_num:
				break
			
			'''Arrival to washer scenario'''
			if current_event == "WashArr":
				if self.isWasherBusy == False:
					self.isWasherBusy = True
					self.wGenDeparture()
					self.wGenArrival()
				else:
					self.washerQ += 1
					self.wGenArrival()
				self.arrived_car_num += 1
			
			'''Departure from washer scenario'''
			if current_event == "WashDep":
				if self.washerQ > 0:
					self.washerQ -= 1
					self.wGenDeparture()
					self.FEL["DryArr"] = self.clock
					self.total_serviced_W += 1
				else:
					self.isWasherBusy = False
					self.FEL["WashDep"] = "---"
					self.FEL["DryArr"] = self.clock
					self.total_serviced_W += 1
				
			'''Arrival to dryer scenario'''
			if current_event == "DryArr":
				if self.isDrierBusy == False:
					self.isDrierBusy = True
					self.dGenDeparture()
					self.FEL["DryArr"] = "---"
				else:
					self.dryerQ += 1
					self.FEL["DryArr"] = "---"
			
			'''Departure from dryer scenario'''
			if current_event == "DryDep":
				if self.dryerQ > 0:
					self.dryerQ -= 1
					self.dGenDeparture()
					self.total_serviced_D += 1
				else:
					self.isDrierBusy = False
					self.FEL["DryDep"] = "---"
					self.total_serviced_D += 1
			
			print"CLOCK: {}        WB(t): {}        WQ(t): {}         DB(t): {}         DQ(t): {}       WA({})   WD({})   DA({})   DD({})\n".format(self.clock, self.isWasherBusy, self.washerQ, self.isDrierBusy, self.dryerQ, self.FEL["WashArr"], self.FEL["WashDep"], self.FEL["DryArr"], self.FEL["DryDep"])


	def stats(self):
		self.avg_time_service_D = float(self.dServiceTime_TOTAL)/self.total_serviced_D
		self.avg_time_service_W = float(self.wServiceTime_TOTAL)/self.total_serviced_W
		self.avg_time_in_sys = self.avg_time_service_D + self.avg_time_service_W
		print "Average time a car spends in the system:\t{}".format(self.avg_time_in_sys)
		print "Utilization of the washer:\t{}".format((self.wServiceTime_TOTAL/self.clock)*100)
		print "Utilization of the dryer:\t{}".format((self.dServiceTime_TOTAL/self.clock)*100)
