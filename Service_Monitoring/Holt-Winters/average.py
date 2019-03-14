#! /usr/bin/python3

# In this script we do a simple implementation of how to calculate the average values of a series
# Example series = [3,10,12,13,12,10,12],
# Therefore the average of the series is 72/7 = 10.29

def average(series):
	return float(sum(series))/len(series)

def main():
	series = [3,10,12,13,12,10,12] 
	print("The average value of the following series: " + str(series) + " is: " + "{0:.2f}".format(average(series)))

main()