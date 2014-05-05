import random, names, time


serviceTimeDistro = [1,1,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,5,5,6]
random.shuffle(serviceTimeDistro)

class Customer(object):

	def __init__(self,arrival_time,service_start_time,service_time):
		self.arrival_time = arrival_time
		self.service_start_time = service_start_time
		self.service_time = service_time
		self.service_end_time = self.service_start_time+self.service_time
		self.waiting_time = self.service_start_time-self.arrival_time
		self.name = names.get_full_name()
		self.total_time = self.service_end_time - self.arrival_time
		if self.waiting_time != 0:
			self.didWait = True
		else:
			self.didWait = False	
	
	def getStats(self):
		print"-----------------------------------------------------------"
		print "{} arrived at {}.".format(self.name, self.arrival_time)
		print "{} waited {} time unit.".format(self.name, self.waiting_time)
		print "{}'s service begin at {}.".format(self.name, self.service_start_time)
		print "{}'s service end at {}.".format(self.name, self.service_end_time)
		print "{} spent {} time unit in the system.".format(self.name, self.total_time)
		print"-----------------------------------------------------------"
	




class Grocery(object):
	def __init__(self):
		self.time = 0
		self.customer_num = input('Enter customer number:\t')
		self.queue = []
		self.customerList = []
		self.idle_time = 0
		
		initialTime = time.clock()
		self.simCheckout()
		finalTime = time.clock()
		timePast = finalTime - initialTime
		print "{} seconds past.".format(timePast)
	
	def simCheckout(self):
		while(True):

			if len(self.customerList) == 0:
				arrival_time = 0
				service_start_time = arrival_time

			else:
				arrival_time += random.randint(1,8)
				service_start_time = max(arrival_time, self.customerList[-1].service_end_time)

			service_time = random.choice(serviceTimeDistro)

			self.customerList.append(Customer(arrival_time, service_start_time, service_time))

			if len(self.customerList) == self.customer_num: break



	def getCustomerStats(self):
		for customer in self.customerList:
			customer.getStats()



	def getGroceryStats(self):
		
		self.avg_total_time = sum([customer.total_time for customer in self.customerList])/float(len(self.customerList))
		self.avg_waiting_time = sum([customer.waiting_time for customer in self.customerList])/float(len(self.customerList))
		self.avg_serv_time = sum([customer.service_time for customer in self.customerList])/float(len(self.customerList))
		
		self.waited_customerList = []
		for customer in self.customerList:
			if customer.didWait is True:
				self.waited_customerList.append(customer)

		self.percent_waited_customer = (float(len(self.waited_customerList))/len(self.customerList))*100
		
		if (len(self.waited_customerList) is not 0):
			self.avg_waiting_time_for_waited_customers = sum([customer.waiting_time for customer in self.waited_customerList])/float(len(self.waited_customerList))
		else:
			self.avg_waiting_time = 0

		self.idle_time = 0
		for current, last in zip(self.customerList[1:], self.customerList):
			if current.arrival_time >= last.service_end_time:
				self.idle_time += current.arrival_time - last.service_end_time

		self.percent_idle_time = (float(self.idle_time)/self.customerList[-1].service_end_time)*100

		self.diff_arrival_times = 0
		for current, last in zip(self.customerList[1:], self.customerList):
			if current.arrival_time >= last.service_end_time:
				self.diff_arrival_times += current.arrival_time - last.arrival_time

		self.avg_time_between_arrivals = float(self.diff_arrival_times)/len(self.customerList)

		print "The average time a customer spends in the system is {} ".format(self.avg_total_time)
		print "The average waiting time of a customer is {}".format(self.avg_waiting_time)
		print "The average service time of a customer is {}".format(self.avg_serv_time)
		print "The percentage of the customers wait at the checkout counter is {}".format(self.percent_waited_customer)
		print "The average waiting time of the customers who wait is {}".format(self.avg_waiting_time_for_waited_customers)
		print "The percentage of the time the checkout counter is idle is {}".format(self.percent_idle_time)
		print "The average time between arrivals to the checkout counter is {}".format(self.avg_time_between_arrivals)












	
