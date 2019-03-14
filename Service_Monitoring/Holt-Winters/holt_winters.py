#! /usr/bin/python3
#Triple Exponential Smoothing a.k.a Holt-Winters Method

'''
The idea behind triple exponential smoothing is to apply exponential smoothing to the seasonal components in addition to 
level and trend. The smoothing is applied across seasons, e.g. the seasonal component of the 3rd point into the season 
would be exponentially smoothed with the the one from the 3rd point of last season, 3rd point two seasons ago, etc. 

In math notation we now have four equations (see footnote):
	* ℓx=α(yx−sx−L)+(1−α)(ℓx−1+bx−1) Level
	* bx=β(ℓx−ℓx−1)+(1−β)bx−1        Trend
	* sx=γ(yx−ℓx)+(1−γ)sx−L			 Season
	* y^x+m=ℓx+mbx+sx−L+1+(m−1)modL  Forecasting

What’s new:
    We now have a third greek letter, γ (gamma) which is the smoothing factor for the seasonal component.
    The expected value index is x+m where m can be any integer meaning we can forecast any 
    number of points into the future (woo-hoo!)

    The forecast equation now consists of level, trend and the seasonal component.

The index of the seasonal component of the forecast sx−L+1+(m−1)modL may appear a little mind boggling, 
but it’s just the offset into the list of seasonal components from the last set from observed data.
'''

import matplotlib.pyplot as plt


'''
HWMinimizeSSE repeatedly executes hwTripleExponentialSmoothing over data, season, slen, trend and nPred with varying α, β and γ 
using the Nelder-Mead algorithm to minimize SSE.  It returns the final (best) smooth and dev returned by 
hwTripleExponentialSmoothing, as well as the resulting α, β, γ (which can be reused later), k (number of passes) 
and e (evocation count for hwTripleExponentialSmoothing).
'''
'''
def hw_minimizeSSE(series, ):
    doit = function(value_array):
        alpha, beta, gamma, sse = value_array[0], value_array[1], value_array[2], 0.0

    #These are 4 initial α, β, γ triplets - TODO these are completely arbitrary?
    #s := [][]float64{{0.1, 0.1, 0.1}, {0.9, 0.9, 0.9}, {0.5, 0.5, 0.5}, {0.1, 0.9, 0.1}}
    #s := [][]float64{{0.1, 0.01, 0.9}, {0.9, 0.1, 0.1}, {0.5, 0.2, 0.5}, {0.1, 0.9, 0.1}}
    #s := [][]float64{{0.1, 0.1, 0.1}, {0.9, 0.9, 0.9}, {0.1, 0.1, 0.9}, {0.9, 0.9, 0.1}}
    #s := [][]float64{{0.1, 0.2, 0.3}, {0.9, 0.8, 0.7}, {0.5, 0.4, 0.3}, {0.1, 0.9, 0.01}}

    triplet = [[0.1, 0.01, 0.9], [0.9, 0.1, 0.1], [0.5, 0.2, 0.5], [0.1, 0.9, 0.1]]

    result = []
    result, num_pases, evocation_count = nelderMeadOptimize(doit, triplet, )
'''


#Initial trend, which is the first season data analysis
#Series that we want to analize trend data, seasons lenght, which is the number of points between seasons
def initial_trend(series, season_len):
    sum = 0.0
    for i in range(season_len):
        sum += float(series[i+season_len] - series[i])/season_len
    return sum / season_len

#Initial seasonal components
def initial_seasonal_component(series, season_len):
    seasonals = {}
    season_averages = []
    n_seasons = int(len(series)/season_len)

    #Now compute season averages
    for j in range(n_seasons):
        season_averages.append(sum(series[season_len*j:season_len*j+season_len])/float(season_len))

    #Now we compute the initial values
    for i in range(season_len):
        sum_of_vals_over_avg = 0.0
        for j in range(n_seasons):
            sum_of_vals_over_avg += series[season_len*j+1] - season_averages[j]
        seasonals[i] = sum_of_vals_over_avg/n_seasons
    return seasonals


def holt_winters(series, alpha, beta, gamma, season_len, n_predictions):
    result = []
    seasonals = initial_seasonal_component(series, season_len)
    
    for i in range(len(series) + n_predictions):
        #Initial values
        if i == 0:
            level = series[0]
            trend = initial_trend(series, season_len)
            result.append(series[0])
            continue
        #We are forecasting
        if i >= len(series):
            m = i - len(series) + 1
            result.append((level+m*trend) + seasonals[i%season_len])
        #We are doing the calculus of the existing values
        else:
            val = series[i]
            last_level, level = level, (alpha*(val-seasonals[i%season_len])) + ((1-alpha)*(level+trend))
            trend = (beta*(level-last_level)+((1-beta)*trend))
            seasonals[i%season_len] = (gamma*(val-level)) + ((1-gamma)*seasonals[i%season_len])
            result.append(level+trend+seasonals[i%season_len])
    return result

def main():
    series = [30,21,29,31,40,48,53,47,37,39,31,29,17,9,20,24,27,35,41,38,
          27,31,27,26,21,13,21,18,33,35,40,36,22,24,21,20,17,14,17,19,
          26,29,40,31,20,24,18,26,17,9,17,21,28,32,46,33,23,28,22,27,
          18,8,17,21,31,34,44,38,31,30,26,32]

    alpha = 0.716 #This value has to be < 1
    beta = 0.029 #This value has to be < 1
    gamma = 0.993 #This value has to be < 1

    season_len = 12
    n_predictions = 24

    hw_series = holt_winters(series, alpha, beta, gamma, season_len, n_predictions)

    print("The single exponential smoothing of the following series: " + str(series) + " is: " + str(hw_series))

    plt.plot(series, marker = 'o', color = 'r')
    plt.plot(hw_series, marker = 'o', color = 'b')
    plt.ylabel('Values')
    plt.xlabel('Data points')
    plt.show()

main()