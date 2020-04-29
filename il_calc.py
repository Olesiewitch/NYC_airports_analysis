import pandas as pd 
import numpy as np 
import il_data


def calc_top_dest(data, n): 
    '''
    calculates following results for the
    given airports:
    - top n destinations with # of 
    flights during given period 

    --------------------------
    data : DataFrame 

    flights data for the selected airports

    n: int 

    nr of top destinations for every airport

    ---------------------------

    returns: Data Frame 
    size : (airports x n top destinations) x(origin, )  
    '''

    ordered = data.groupby(['origin', 'city', 'destination']
            )['departure'].agg( ['count']).sort_values(
                'count', ascending=False).reset_index()


    results = ordered.groupby('origin').head(n)

    return results


def basic_stat(data): 
    '''
    reports basic statistics for 
    the airports such as: 
    - % of international flights
    - # of destinations
    - total # of flights

    ---------------------
    data : DataFrame 

    flights data 
    ---------------------

    returns dataframe 
    '''
    results = pd.DataFrame(index =data['origin'].unique())
    

    for a in results.index:
        air_data = data.loc[data['origin'] == a,:]
        results.loc[a, 'international'] = str(round((sum(air_data['int'])  \
                                    /air_data.shape[0] * 100), 2)) +' %'  
        results.loc[a,'total flight'] = air_data.shape[0]
        results.loc[a,'total destinations'] = len(air_data['city'].unique())
   
    return results 



def airline_stat(data): 
    ''' returns the total number of fliths performed 
    by each airline at each of the origin airports. 

    -----------------------------------------------
    data: DataFrame

    flights data

    -----------------------------------------------
    returns: DataFrame 

    size: (# airports x # airlines) x 1 (# of flights)  


    '''
  
    stats= data.groupby(['origin', 
        'name'])['destination'].agg('size').reset_index(
        ).rename(columns = {'destination': 'count'})

    return stats    

def monthly_data(flights, airport): 
    '''
    '''

    data= flights.loc[flights['origin']==airport]
    results = pd.DataFrame(columns= [1.0, 2.0, 3.0, 4.0, 5.0,
                         6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0])
   

    for m in results.columns: 
        month_data = data.loc[data['month']== m]

        if len(month_data['delay']) != 0 : 
            results.loc['monthly_delays', m] = (sum(month_data['delay']) / len(
                month_data['delay']))*100
        else: 
            results.loc['monthly_delays', m] = 0

        if len(month_data.loc[month_data['delay_min'] >15 , 
                                        'delay_min']) != 0:                            
            results.loc['total_delays', m] = len(
                                      month_data.loc[month_data['delay_min'] >15 ,
                                       'delay_min'])
        else:
             results.loc['total_delays', m] = 0
    
    return results     



        