#!/usr/bin/python3

# simple average calculation
def average(series):
	return float(sum(series))/len(series)

# moving average using the last n points
def moving_average(series, n):
	return average(series[-n:])

# weighted average, weights is a list of weights
def weighted_average(series, weights):
	result = 0.0
	weights.reverse()
	for n in range(len(weights)):
		result += series[-n-1] * weights[n]
	return result

# given a series and alpha, return series of smoothed points
def exponential_smoothing(series, alpha):
	result = [series[0]] #first values is same as series
	for n in range(1, len(series)):
		result.append(alpha * series[n] + (1 - alpha) * result[n-1])
	return result

series = [3,10,12,13,12,10,12]
weights = [0.1, 0.2, 0.3, 0.4]

print("The average of the series is: " + "{0:.2f}".format(average(series)))
print("The moving average of the series, given the last 3 points: " + "{0:.2f}".format(moving_average(series, 3)))
print("The weighted average of the series, given a weight list: " + "{0:.2f}".format(weighted_average(series, weights)))
print("The exponential smoothing of the series, given an alpha of 3: " + str(exponential_smoothing(series, 0.9)))