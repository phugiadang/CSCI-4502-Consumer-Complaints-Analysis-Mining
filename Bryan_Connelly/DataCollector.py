import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model

class DataCollector:
	def __init__(self):
		# self.annualComplaints = {'AL': [], 'AK': [], 'AZ': [], 'AR': [], 'CA': [], 'CO': [], 'CT': [], 'DE': [], 'FL': [], 'GA': [], 'HI': [], 'ID': [], 'IL': [], 'IN': [], 'IA': [], 'KS': [], 'KY': [], 'LA': [], 'ME': [], 'MD': [], 'MA': [], 'MI': [], 'MN': [], 'MS': [], 'MO': [], 'MT': [], 'NE': [], 'NV': [], 'NH': [], 'NJ': [], 'NM': [], 'NY': [], 'NC': [], 'ND': [], 'OH': [], 'OK': [], 'OR': [], 'PA': [], 'RI': [], 'SC': [], 'SD': [], 'TN': [], 'TX': [], 'UT': [], 'VT': [], 'VA': [], 'WA': [], 'WV': [], 'WI': [], 'WY': [], 'DC': []}
		self.annualComplaintsByProduct = {'AL': [], 'AK': [], 'AZ': [], 'AR': [], 'CA': [], 'CO': [], 'CT': [], 'DE': [], 'FL': [], 'GA': [], 'HI': [], 'ID': [], 'IL': [], 'IN': [], 'IA': [], 'KS': [], 'KY': [], 'LA': [], 'ME': [], 'MD': [], 'MA': [], 'MI': [], 'MN': [], 'MS': [], 'MO': [], 'MT': [], 'NE': [], 'NV': [], 'NH': [], 'NJ': [], 'NM': [], 'NY': [], 'NC': [], 'ND': [], 'OH': [], 'OK': [], 'OR': [], 'PA': [], 'RI': [], 'SC': [], 'SD': [], 'TN': [], 'TX': [], 'UT': [], 'VT': [], 'VA': [], 'WA': [], 'WV': [], 'WI': [], 'WY': [], 'DC': []}
		self.annualPop = []
		self.states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC']
		self.product = ''

		self.monthlyComplaintsByProduct = {}
		self.monthlyPop = []

	def printMonthlyComplaintsByProduct(self):
		for month in self.monthlyComplaintsByProduct:
			print 'Month: ' + str(month) + ', Complaints: ' + str(self.monthlyComplaintsByProduct[month])

	def readMonthlyComplaintsByProduct(self, complaint_product):
		with open('Consumer_Complaints.csv', 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')

			first = True
			for row in reader:
				#skip the first row
				if first:
					first = False
					continue

				#get date in YYYYMM format
				comp_date = row[0].translate(None, '/')
				comp_date = comp_date[4] + comp_date[5] + comp_date[6] + comp_date[7] + comp_date[0] + comp_date[1]

				#skip anything from 2011 or 2016
				if int(comp_date) > 201600 or int(comp_date) < 201200:
					continue

				#make sure the complaint type is right
				if complaint_product == 'all':
					try:
						self.monthlyComplaintsByProduct[comp_date] += 1
					except:
						self.monthlyComplaintsByProduct[comp_date] = 1

				elif row[1] == complaint_product:
					try:
						self.monthlyComplaintsByProduct[comp_date] += 1
					except:
						self.monthlyComplaintsByProduct[comp_date] = 1

	def readMonthlyPop(self):
		with open('Monthly_Pop.csv', 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter='	')
			for row in reader:
				self.monthlyPop.append(row[1])

	def printMonthlyPop(self):
		years = ['2011', '2012', '2013', '2014', '2015', '2016']
		yearIndex = 0
		i = 0
		while i < len(self.monthlyPop):
			if i%12 == 0:
				print '\n' + years[yearIndex]
				yearIndex += 1
			print self.monthlyPop[i]
			i += 1

	def readStateAnnualPop(self):
		with open('AnnualPopulation.csv', 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			first = True
			for row in reader:
				if first == True:
					first = False
					continue

				self.annualPop.append([int(row[6]), int(row[5]), int(row[4]), int(row[3])])


	def printStateAnnualPop(self):
		print '\nState Populations:'
		i = 0
		for state in self.annualPop:
			print self.states[i] + ': ' + str(state[0]) + ', ' + str(state[1]) + ', ' + str(state[2]) + ', ' + str(state[3])
			i += 1
	
	# def readStateAnnualComplaints(self):
	# 	with open('Consumer_Complaints.csv', 'r') as csvfile:
	# 		reader = csv.reader(csvfile, delimiter=',')

	# 		years = ['2015', '2014', '2013', '2012']
	# 		i = 0
	# 		for year in years:
	# 			print year
	# 			first = True
	# 			for row in reader:
	# 				comp_date = row[0].translate(None, '/')
	# 				#make sure we're in the right year and don't read the first line of labels in the file
	# 				if first == True or (comp_date[4] + comp_date[5] + comp_date[6] + comp_date[7]) != year:
	# 					first = False
	# 					continue
	# 				#make sure we're only looking at US states and DC
	# 				if row[8] not in ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC']:
	# 					continue

	# 				#if this is the first complaint for the year, append a new number. Otherwise increment the existing number
	# 				if len(self.annualComplaints[row[8]]) == i:
	# 					self.annualComplaints[row[8]].append(1)
	# 				elif row[1] == complaint_product:
	# 					self.annualComplaints[row[8]][i] += 1
	# 			i += 1
	# 			csvfile.seek(0)

	def printStateAnnualComplaints(self):
		print 'State Complaints: '
		for state in self.annualComplaints:
			print state + ': ' + str(self.annualComplaints[state])

	def readStateAnnualComplaintsByProduct(self, complaint_product):
		self.product = complaint_product
		with open('Consumer_Complaints.csv', 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')

			years = ['2015', '2014', '2013', '2012']
			i = 0
			for year in years:
				first = True
				for row in reader:
					comp_date = row[0].translate(None, '/')
					#make sure we're in the right year and don't read the first line of labels in the file
					if first == True or (comp_date[4] + comp_date[5] + comp_date[6] + comp_date[7]) != year:
						first = False
						continue
					#make sure we're only looking at US states and DC
					if row[8] not in ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC']:
						continue
					#make sure we're looking at the right complaint
					if complaint_product != 'all':
						#if this is the first complaint for the year, append a new number. Otherwise increment the existing number
						if row[1] == complaint_product and len(self.annualComplaintsByProduct[row[8]]) == i:
							#print self.annualComplaints[row[8]]
							self.annualComplaintsByProduct[row[8]].append(1)
						elif row[1] == complaint_product:
							self.annualComplaintsByProduct[row[8]][i] += 1
					#if we don't care about the complaint type, do the same thing but don't check row[1]
					else:
						#if this is the first complaint for the year, append a new number. Otherwise increment the existing number
						if len(self.annualComplaintsByProduct[row[8]]) == i:
							#print self.annualComplaints[row[8]]
							self.annualComplaintsByProduct[row[8]].append(1)
						else:
							self.annualComplaintsByProduct[row[8]][i] += 1
				i += 1
				csvfile.seek(0)

	def printStateAnnualComplaintsByProduct(self):
		print 'State Complaints By Product (' + self.product + '): '
		for state in self.annualComplaintsByProduct:
			print state + ': ' + str(self.annualComplaintsByProduct[state])

	def printAnnualPopComp(self):
		i = 0
		while i < 51:
			print str(self.annualPop[i][0]) + ': ' + str(self.annualPop[i][1]) + ', ' + str(self.annualPop[i][2]) + ', ' + str(self.annualPop[i][3]) + ', ' + str(self.annualPop[i][4])
			print self.states[i] + ': ' + str(self.annualComplaints[self.states[i]])
			i += 1

	def minMaxNormalized(self,data):
		min_data = float(min(data))
		max_data = float(max(data))
		normalized = []
		for num in data:
			normalized.append((float(num) - min_data)/(max_data - min_data))
		return normalized

	def graphTotals(self):
		total_pop = [0, 0, 0, 0]
		total_comp = [0, 0, 0, 0]
		yr = 0

		while yr < 4:
			for state in self.annualPop:
				pop = int(state[yr])
				#print state + ' ' + str(pop)
				total_pop[yr] += pop 
			yr += 1

		yr = 0

		while yr < 4:
			for state in self.annualComplaints:
				total_comp[yr] += self.annualComplaintsByProduct[state][yr]
			yr += 1

		total_pop = self.minMaxNormalized(total_pop)
		total_comp = self.minMaxNormalized(total_comp)

		plt.plot(total_comp, c='blue')
		plt.plot(total_pop, c='green')
		plt.show()



