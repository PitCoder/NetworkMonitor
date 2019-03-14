#! /usr/bin/python3

# In this script we show how to implement a function that calculate the moving average of a series
# Example series = [3,10,12,13,12,10,12], moving factor = 3
# Then moved_series = [12,10,12]
# Therefore the average of the moved_series is 34/3 = 11.33

from average import average

def moving_average(series, n):
	return average(series[-n:])

def main():
	series = [3,10,12,13,12,10,12] 
	n = 3
	print("The moving average value of the following series: " + str(series) + " is: " + "{0:.2f}".format(moving_average(series, n)))

main()