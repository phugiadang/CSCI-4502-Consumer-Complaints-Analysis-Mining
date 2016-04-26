import operator
import sys
import numpy as np
import matplotlib.pyplot as plt
from LinearRegressionObject import LinearRegressionObject
from DataCollector import DataCollector

if len(sys.argv) != 2 or sys.argv[1] not in ['all', 'Bank account or service', 'Debt collection', 'Mortgage', 'Consumer Loan', 'Credit reporting', 'Credit card', 'Student loan', 'Payday loan', 'Prepaid card', 'Money transfers', 'Other financial service']:
	print 'Usage: python ComplaintsvsPopulation.py <product>'
	print "where <product> is 'Bank account or service', 'Debt collection', 'Mortgage', 'Consumer Loan', 'Credit reporting', 'Credit card', 'Student loan', 'Payday loan', 'Prepaid card', 'Money transfers', 'Other financial service'"

else:

	collector = DataCollector()
	collector.readMonthlyPop()
	collector.readMonthlyComplaintsByProduct(sys.argv[1])
	# collector.printMonthlyComplaintsByProduct()

	comp_dic = collector.monthlyComplaintsByProduct
	pop_array = map(int, collector.monthlyPop)
	sorted_comp_tuples = sorted(comp_dic.items(), key=operator.itemgetter(0))
	sorted_comp = []
	all_months = []
	for tup in sorted_comp_tuples:
		all_months.append(tup[0])
		sorted_comp.append(tup[1])

	linreg = LinearRegressionObject(pop_array, sorted_comp, 'National')
	text, data = linreg.linearRegressionAnalysis()
	correl = linreg.rawCorrelationCalculation()

	print 'National Monthly Correlation: ' + str(correl)
	print text