import pandas as pd 
import numpy as np 
import il_data
import il_calc 
import il_graph
import statsmodels.formula.api as smf
import statsmodels.api as sm


## PARSING AND CLASSIFING THE DATA 

NY_airports = ['JFK', 'LGA']

NY_flights = il_data.get_flights_data(NY_airports)

flights_data = il_data.classify_flights(NY_flights)


### BASIC STATISTICAL REVIEW AND GRAPHS  

basic_stats = il_calc.basic_stat(flights_data)

dest_data = il_calc.calc_top_dest(flights_data, 5)

airlines_data = il_calc.airline_stat(flights_data)
print(airlines_data.loc[airlines_data['origin']==NY_airports[0]])
print(airlines_data.loc[airlines_data['origin']==NY_airports[1]])

il_graph.airlines_break_down(airlines_data, NY_airports[0])
il_graph.airlines_break_down(airlines_data, NY_airports[1])

il_graph.top_des(dest_data, NY_airports[0], 'steelblue')
il_graph.top_des(dest_data, NY_airports[1], 'seagreen')

monthly_LGA = il_calc.monthly_data(flights_data, NY_airports[0])
monthly_JFK = il_calc.monthly_data(flights_data, NY_airports[1])


il_graph.monthly_delays(monthly_LGA, NY_airports[0])
il_graph.monthly_delays(monthly_JFK, NY_airports[1])




### STATISTICAL ANALYSIS OF THE DELAYS :LOGIT

f = 'delay ~ C(carrier) + C(origin) + '+ 'C(month) + ' +  \
 '+ C(country)'

logitfit = smf.logit(formula = str(f), data =  \
        flights_data).fit(method = 'bfgs')

print(logitfit.summary())
print(np.exp(logitfit.params))




