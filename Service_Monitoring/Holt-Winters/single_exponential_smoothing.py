#! /usr/bin/python3
#Single Exponential Smoothing

'''
Similar to weighted average, only with the diference that we consider all of data points, while assigning exponentially smaller
weights as we go back in time, eventually approaching the big old zero, the weights are dictated by math and decay uniformly.
The smaller the starting weight, the faster it approaches to zero.
'''

#Formula: y^x=α⋅yx+(1−α)⋅y^x−1
# α is considered the smoothing factor or smoothing coefficient
#Perhaps α would be better referred to as memory decay rate: the higher the α, the faster the method “forgets”.

import matplotlib.pyplot as plt

def exponential_smoothing(series, alpha):
	result = []
	for i in range(len(series)):
		result.append(alpha * series[i] + (1 - alpha) * series[i-1])
	return result

def main():
	series = [3,10,12,13,12,10,12] 
	alpha = 0.9 #This value has to be < 1
	ses_series = exponential_smoothing(series, alpha)

	print("The single exponential smoothing of the following series: " + str(series) + " is: " + str(ses_series))

	plt.plot(series, marker = 'o', color = 'r')
	plt.plot(ses_series,  marker = 'o', color = 'b')
	plt.ylabel('Values')
	plt.xlabel('Data points')
	plt.show()
main()

#Why is it called “smoothing”?
#To the best of my understanding this simply refers to the effect these methods have on a graph 
#if you were to plot the values: jagged lines become smoother. 

#Moving average also has the same effect, so it deserves the right to be called smoothing just as well.