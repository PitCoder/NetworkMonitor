'''
Contraint optimization - A quick insight

Most (if not all) economic decisions are the result of an optimization problem, subject to one or a series of constraints

    1.- Consumers make decisions on what to buy constrained by the fact that their choice must be affordable.
    2.- Firms make production decisions to maximize their profits subject to the constraint that they have limited production capacity.
    3.- Households make decisions on how much to work/play with the constraint that there are only so many hours in the day.
    4.- Firms minimize cost subject to the constraint that they have order to fulfill.

    All of these problem fall under the category of constrained optimization. Luckily, Tthre is a uniform process that we can use to solve these problems:

    Maximizing Subject to a set of constraints:

    max x,y f(x, y)
    subject to g(x, y) >= 0 

    Note: By optimizing Holt-Winters function we are maximizing the possible values that alpha, beta and gamma can have, this means that we have an optimization problem given 3 variables.

    max α,β,γ f(α, β, γ)
    subject to 0 <= α, β, γ <= 1
'''


# The first thing we have to do is to compute the predicted y values for a given α, β or γ and spit out an 
# error (Say SSE of y_predicted and y)

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

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

def error_function(input_params, series, season_len, n_predictions):
    α, β, γ = input_params
    #We call the Holt-Winters implementation with α, β and γ
    forecast_series = holt_winters(series, α, β, γ, season_len, n_predictions)

    #We compute different error metrics
    sse = 0 #SSE - Square Standard Error

    for i in range(n_predictions, len(series)):
        sse += (forecast_series[i] - series[i]) **  2

    return sse


def main():
    #Original values for α, β and γ
    α = 0.8
    β = 0.1
    γ = 0.1

    #Proposed values for α, β and γ
    αp = 0.716
    βp = 0.029
    γp = 0.993

    series = [30,21,29,31,40,48,53,47,37,39,31,29,17,9,20,24,27,35,41,38,
          27,31,27,26,21,13,21,18,33,35,40,36,22,24,21,20,17,14,17,19,
          26,29,40,31,20,24,18,26,17,9,17,21,28,32,46,33,23,28,22,27,
          18,8,17,21,31,34,44,38,31,30,26,32]

    season_len = 12
    n_predictions = 24

    #We define a parameter list formed by the given values
    param_list = [α, β, γ] 

    #We define the bounds for each values: In Holt-Winters method this range from 0 to 1
    bounds = ((0,1), (0,1), (0,1)) #This is a tuple sice these values are constant

    '''
    We make use of the library scipy in order to do the constrained minimization of multivariate 
    scalar functions (minimize) using a variety of algorithms (e.g. BFGS, Nelder-Mead simplex,
    Newton Conjugate Gradient, COBYLA or SLSQP)
    '''
    optimized_params = minimize(error_function, param_list, bounds = bounds, args = (series, season_len, n_predictions), method = "L-BFGS-B")
    print(optimized_params.x)
    αo, βo, γo = optimized_params.x

    print(αo)
    print(βo)
    print(γo)

    #Here we plot the original series
    plt.plot(series, marker = 'o', color = 'r')

    #Here we plot the series with the trial-error values
    hw_series = holt_winters(series, αp, βp, γp, season_len, n_predictions)
    plt.plot(hw_series, marker = 'o', color = 'b')

    #Here we plot the series with the optimization values}
    opt_hw_series = holt_winters(series, αo, βo, γo, season_len, n_predictions)
    plt.plot(opt_hw_series, marker = 'o', color = 'g')


    plt.ylabel('Values')
    plt.xlabel('Data points')
    plt.show()

if __name__ == "__main__":
    main()