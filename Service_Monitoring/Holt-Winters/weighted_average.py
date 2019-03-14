#! /usr/bin/python3

# In this script we show how to implement a function that calculate the weighted average of a series
# Example series = [3,10,12,13,12,10,12], weighted values = weights = [0.1, 0.2, 0.3, 0.4]
# Then the weights reversed = [0.4, 0.3, 0.2, 0.1]
# Inside the for loop, we are 
# Iteration no. 1: 0 += 12 * 0.4
# Iteration no. 2: 4.8 += 10 * 0.3
# Iteration no. 3: 7.8 += 12 * 0.2
# Iteration no. 4: 10.2 += 13 * 0.1
# Moving average = 11.5

from average import average

def weighted_average(series, weights):
	result = 0.0
	weights.reverse()
	for i in range(len(weights)):
		result += series[-i-1] * weights[i]
	return result

def main():
	series = [3,10,12,13,12,10,12]
	weights = [0.1, 0.2, 0.3, 0.4]
	print("The weighted average value of the following series: " + str(series) + " is: " + "{0:.2f}".format(weighted_average(series, weights)))

main()