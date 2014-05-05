import numpy as np
import random
import matplotlib.pyplot as plt
import math


class Methods(object):
    def __init__(self):
        self.random_num_list = [ ]
        self.seed_one = None
        self.constant = None
        self.mod = None
        self.a = None
        self.seed_list = [ ]
        self.factor = None
        pass

    
    def Midsquare(self):
        self.random_num_list = [ ]
        self.N = input("How many random number will be produced?: \n")
        while True:
            self.seed_one = input("Enter a four digit number for seed: \n")
            if len(str(self.seed_one)) >= 4:
                break
            else:
                print "Invalid Input! \n"
        while len(self.random_num_list) <= self.N:
            dummy = str(int(math.pow(self.seed_one, 2)))   
            if len(dummy) % 2 != 0:
                dummy = "0" + dummy
            self.seed_one = int(dummy[((len(dummy)/2)-2):((len(dummy)/2)+2)])
            self.random_num_list.append(self.seed_one/10000.0)
        histo, bin_edges = np.histogram(self.random_num_list, bins=20)
        plt.bar(bin_edges[:-1], histo, width=0.05) 
        plt.xlim(min(bin_edges),max(bin_edges))
        plt.show()
    

    def Midproduct(self):
        self.random_num_list = [ ]
        self.N = input("How many random number will be produced?: \n")
        while True:    
            self.seed_one = input("Enter the first seed (atleast 4-digit): \n")
            self.seed_two = input("Enter the second seed (atleast 4-digit): \n")
            if ((len(str(self.seed_one)) >= 4) and (len(str(self.seed_two)) >= 4)):
                break
            else:
                print "Invalid Input! \n"
        while len(self.random_num_list) <= self.N:
            dummy = str(self.seed_one * self.seed_two)
            if len(dummy) % 2 != 0:
                dummy = "0" + dummy
            self.seed_one = self.seed_two
            self.seed_two = int(dummy[((len(dummy)/2)-2):((len(dummy)/2)+2)])
            self.random_num_list.append(self.seed_two/10000.0)
        histo, bin_edges = np.histogram(self.random_num_list, bins=20)
        plt.bar(bin_edges[:-1], histo, width=0.05) 
        plt.xlim(min(bin_edges),max(bin_edges))
        plt.show()


    def ConstantMultiplier(self):
        self.random_num_list = [ ]
        self.N = input("How many random number will be produced?: \n")
        while True:    
            self.constant= input("Enter the constant (Any digit): \n")
            self.seed_one = input("Enter the seed (atleast 4-digit): \n")
            if len(str(self.seed_one)) >= 4:
                break
            else:
                print "Invalid Input! \n"
        while len(self.random_num_list) <= self.N:
            dummy = str(self.seed_one * self.constant)
            if len(dummy) % 2 != 0:
                dummy = "0" + dummy
            self.seed_one = int(dummy[((len(dummy)/2)-2):((len(dummy)/2)+2)])
            self.random_num_list.append(self.seed_one/10000.0)
        histo, bin_edges = np.histogram(self.random_num_list, bins=20)
        plt.bar(bin_edges[:-1], histo, width=0.05) 
        plt.xlim(min(bin_edges),max(bin_edges))
        plt.show()

    def AdditiveCongrential(self):
        self.random_num_list = [ ]
        self.N = input("How many random number will be produced?: \n")
        self.mod = input("Enter mod: \n")
        self.seed_list = [ ] # Reset the list.
        i = 0
        while True:
            dummy = input("Enter value of the seed (-1 to quit): ")
            if dummy == -1 :
                break
            else:
                self.seed_list.append(dummy)
        while len(self.random_num_list) <= self.N: 
            self.seed_list.append((self.seed_list[i] + self.seed_list[-1])%self.mod)
            self.random_num_list.append(float(self.seed_list[-1])/self.mod)
            i = i + 1 
        histo, bin_edges = np.histogram(self.random_num_list, bins=20)
        plt.bar(bin_edges[:-1], histo, width=0.05) 
        plt.xlim(min(bin_edges),max(bin_edges))
        plt.show()

   
    def LinearCongurential(self):
        self.random_num_list = [ ]
        self.N = input("How many random number will be produced?: \n")
        self.mod = input("Enter mod: \n")
        self.seed_one = input("Enter the seed: \n")
        self.factor = input("Enter the factor: \n")   
        self.constant = input("Enter the constant: \n")
        while len(self.random_num_list) <= self.N:
            self.seed_one  = (((self.factor * self.seed_one) + self.constant))%self.mod
            self.random_num_list.append(self.seed_one/float(self.mod))
        histo, bin_edges = np.histogram(self.random_num_list, bins=20)
        plt.bar(bin_edges[:-1], histo, width=0.05) 
        plt.xlim(min(bin_edges),max(bin_edges))
        plt.show()


