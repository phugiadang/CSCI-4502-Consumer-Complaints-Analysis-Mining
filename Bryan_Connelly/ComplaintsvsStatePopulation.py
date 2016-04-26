import sys
import numpy as np
from sklearn import linear_model
# import matplotlib as mpl
# mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from LinearRegressionObject import LinearRegressionObject
from DataCollector import DataCollector

if len(sys.argv) != 2 or sys.argv[1] not in ['all', 'Bank account or service', 'Debt collection', 'Mortgage', 'Consumer Loan', 'Credit reporting', 'Credit card', 'Student loan', 'Payday loan', 'Prepaid card', 'Money transfers', 'Other financial service']:
	print 'Usage: python ComplaintsvsPopulation.py <product>'
	print "where <product> is 'Bank account or service', 'Debt collection', 'Mortgage', 'Consumer Loan', 'Credit reporting', 'Credit card', 'Student loan', 'Payday loan', 'Prepaid card', 'Money transfers', 'Other financial service'"

else:

	states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC']

	collector = DataCollector()
	collector.readStateAnnualPop()

	#options for products:
	#'Bank account or service', 'Debt collection', 'Mortgage', 'Consumer Loan', 
	#'Credit reporting', 'Credit card', 'Student loan', 'Payday loan', 'Prepaid card',
	#'Money transfers', 'Other financial service'
	collector.readStateAnnualComplaintsByProduct(sys.argv[1])

	#run the linear regression on each state
	comp_dic = collector.annualComplaintsByProduct
	pop_array = collector.annualPop

	i = 0
	#get the average correlation between the data across all the states
	avg_correl = 0
	for state in states:
		complaint = comp_dic[state]
		population = pop_array[i]
		linreg = LinearRegressionObject(population, complaint, 'state_images/' + state)
		text, data = linreg.linearRegressionAnalysis()
		correl = linreg.rawCorrelationCalculation()
		print state + ' Correlation: ' + str(correl)
		avg_correl += float(correl)
		i += 1
	avg_correl = avg_correl/len(states)
	print 'Average Correlation: ' + str(avg_correl)