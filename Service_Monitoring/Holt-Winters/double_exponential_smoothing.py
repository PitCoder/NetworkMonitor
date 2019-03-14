#! /usr/bin/python3
#Double Exponential Smoothing

'''
So now we have two components to a series: level and trend. In Part I we learned several methods to forecast the level, 
and it should follow that every one of these methods can be applied to the trend just as well.

E.g. the naive method would assume that trend between last two points is going to stay the same, or we could average 
all slopes between all points to get an average trend, use a moving trend average or apply exponential smoothing.

Double exponential smoothing then is nothing more than exponential smoothing applied to both level and trend. 
To express this in mathematical notation we now need three equations: 
	* one for level
	* one for the trend
	* one to combine the level and trend to get the expected y^.
'''

#Formulas:
# ℓx=αyx+(1−α)(ℓx−1+bx−1) Level
# bx=β(ℓx−ℓx−1)+(1−β)bx−1 Trend
# y^x+1=ℓx+bx 			  Forecast

import matplotlib.pyplot as plt

def double_exponential_smoothing(series, alpha, beta):
	result = [series[0]] #The series must have at least 1 value to be able to do forecasting
	for n in range(1, len(series) + 1): #The series start at 1 because we interested in the next value that we are seeing
		#Actual first level and trend calculation
		if(n == 1):
			level, trend = series[0], series[1] - series[0]
		#We are forecasting
		if n >= len(series):
			value = result[-1]
		#We take the actual value
		else:
			value = series[n]
		
		#Last level calculation
		last_level, level = level, (alpha*value) + ((1-alpha)*(level+trend))
		#Last trend calculation
		last_trend, trend = trend, (beta*(level - last_level)) + ((1 - beta)*trend)
		#Forecast
		result.append(last_level + last_trend)
	return result

def main():
	series = [3,10,12,13,12,10,12] 
	alpha = 0.9 #This value has to be < 1
	beta = 0.9 #This value has to be < 1
	des_series = double_exponential_smoothing(series, alpha, beta)

	print("The single exponential smoothing of the following series: " + str(series) + " is: " + str(des_series))
	
	plt.plot(series, marker = 'o', color = 'r')
	plt.plot(des_series, marker = 'o', color = 'b')
	plt.ylabel('Values')
	plt.xlabel('Data points')
	plt.show()

main()

