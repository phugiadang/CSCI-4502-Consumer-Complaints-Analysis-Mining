import numpy as np
from sklearn import linear_model
# import matplotlib as mpl
# mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

class LinearRegressionObject():
	
	#fixed_para_one: name of candidate
	#fixed_para_two: list of dates
	#population: list (source, list of counts) for x-values
	#complaints: list (source, list of counts) for y values
	def __init__(self, population, complaints, name):
		self.population = population
		self.complaints = complaints
		self.name = name
	
	def rawCorrelationCalculation(self):
		return np.corrcoef(self.population,self.complaints)[0][1]	

	#use to calculate the corellation between two data sets
	def correlationCalculation(self):
		correl = np.corrcoef(self.population,self.complaints)[0][1]

		if (correl == 0):
			return "Two variable sets are uncorrelated.\n"
		elif (correl > 0):
			return "There is a positive correlation: one variable set moves the the same direction by "+str(abs(correl))+" the amount that the other variable set moves.\n"
		else:
			return "There is a negative correlation: one variable set moves the the opposite direction by "+str(abs(correl))+" the amount that the other variable set moves.\n"  
			
	
	def __graphData(self, data,slope,intercept,training):
		data.plot(kind='scatter', x='population', y='complaints')
		x_eval = self.population[training:]
		y_eval = self.complaints[training:]
		b = plt.scatter(x_eval,y_eval,c='yellow')
		x = []
		y = []
		for k in self.population:
			x.append(k)
			y_value = slope * k + intercept
			y.append(y_value)
		line, = plt.plot(x,y,c='red',linewidth=2)
		plt.savefig(self.name + '_population'+'_complaints')
	
	#Return the tuples of (report,(date,predict values, exact values))
	def linearRegressionAnalysis(self):
		text_output = "LINEAR REGRESSION ANALYSIS\n"
		text_output = text_output + self.correlationCalculation()
		fixed_para_two = self.complaints
		if text_output != "Two variable sets are uncorrelated.\n":
			training = int(len(self.population)*80/100)
			text_output = text_output + "Training data is from "+str(self.complaints[0])+" to "+str(self.complaints[training-1])+".\n"
			text_output = text_output + "Evaluation data is from "+str(self.complaints[training])+" to "+str(self.complaints[len(self.complaints)-1])+".\n"
			regr = linear_model.LinearRegression()
			dic = {'complaints':self.complaints[:training-1],'population':self.population[:training-1]}
			data = pd.DataFrame(dic)
			data.index += 1
			X = data[['population']]
			y = data['complaints']
			text_output = text_output + "x value is " + 'Population' + "\n"
			text_output = text_output + "y value is " + 'Complaints' + "\n"
			regr.fit(X,y)
			slope = regr.coef_[0]
			intercept = regr.intercept_
			text_output = text_output + "Coefficient computes from linear regression model:\n" + 'Population' + ", " + str(slope) + "\n"
			text_output = text_output + "Interception computes from linear regression model:\n" + 'Population' + ", " + str(intercept) + "\n"
			text_output = text_output + "Linear approximation line has form: y = " + str(slope) + " x + " + str(intercept) + "\n"
			dic_eval = {'complaints': self.complaints[training:],'population': self.population[training:]}
			data_eval = pd.DataFrame(dic_eval)
			data_eval.index += 1
			X_eval = data_eval[['population']]
			y_eval = data_eval['complaints']
			mean_sqr_err = np.mean((regr.predict(X_eval)-y_eval)**2)
			#score = regr.score(X_eval,y_eval)
			text_output = text_output + "Mean square error is " + str(mean_sqr_err) + "\n"
			#text_output = text_output + "Score of this prediction " + str(score) + "\n"
			#text_output = text_output + "(Note: if score number equals 1, there is a perfect prediction and a strong linear relationship between two variables)\n"
			self.__graphData(data,slope,intercept,training)
			y_exact = self.complaints[training:]
			y_predict = []
			date = []
			for x in range (training,len(fixed_para_two)):
				date.append(fixed_para_two[x])
				y_predict.append(int(slope*int(self.population[x])+intercept))
			return (text_output,(date,y_predict,y_exact))


# linreg = LinearRegressionObject([100, 110, 120, 130, 140, 150, 160, 170, 180, 190], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
# text, data = linreg.linearRegressionAnalysis()
# print text
# print data