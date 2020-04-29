import pandas as pd
import numpy as np
import logging 
import io
import urllib.request
import requests 

logging.basicConfig(level=logging.INFO)


def get_flights_data(airports): 
    ''' extracts data flights information for
    specified airports from the flight.csv file.
    The observiations with NAN valued are removed. 
    ------------------------
    airports: list 

    acronym(s) of the airport(s) for which data 
    should be returned.

    ------------------------

    return : Dataframe (n x 9) 
    '''
    data = pd.read_csv('flights.csv')

    data = data[(data['origin'].isin(airports))]

    data['origin'] = data['origin'].astype('category')
    data['destination'] = data['destination'].astype('category')
    data['carrier'] = data['carrier'].astype('category')
    

    
    na_nr = len(data.loc[data.isna().sum(axis = 1)!=0])

    logging.info(' ' + str(na_nr)  + ' observations contiaing NAN ' 
                + 'values were removed (' 
                + str(round((na_nr/data.shape[0] * 100),2)) + '%)')

    data = data.dropna(how = 'any')
    
    logging.info(' Adjusting time data to appropriate format... ')

    data= data.replace(' 24:',' 00:', regex=True )
    data = data.replace('-02-29',' -02-28:', regex=True )
    
    time_data = ('departure', 'scheduled_departure',
                'arrival', 'scheduled_arrival')
    
    
    for c in time_data: 
        data[c] = pd.to_datetime(data[c],
                format = "%Y-%m-%d %H:%M:%S",
                errors='coerce')            
   
    return data


def get_dest_data(flights):
    '''
    downloads the airport data from openflight.org, 
    selects destination airports in @flights and 
    classifies them to domestic and
    internationals airports 

    ---------------------
    flights : DataFrame

    Dataframe with the flights information

    ----------------------

    returns : airports Dataframe (nr of destinations x 6 )

    columns : 'Name', 'City', 'Country', 'Latitude',
              'Longitude', 'Int' (0 - dmstc , 1 - int)
    
    '''
    logging.info(' Obtaining the airport destination' +
                ' data from openflight.com...')

    url = 'https://raw.githubusercontent.com/jpatokal/' +  \
        'openflights/master/data/airports.dat'
    s=requests.get(url).content
    

    airports = pd.read_table(io.StringIO(s.decode('utf-8')), 
            header = None, sep = ',', index_col = 3, 
            usecols = [1,2,3,4,6,7])

    airports.columns = [ 'Name', 'City', 'Country', 'Latitude',
                    'Longitude']

    dest_airports = flights['destination'].unique()

    airports = airports.loc[airports.index.isin(dest_airports)]
    airports['Int'] = np.where(airports['Country'] == 
                    'United States', 0, 1)

    return airports


def classify_delay(row):
    ''' returns number of minutes of delay. 
    Returns negative number of early departutes
    
    '''
    
    if row['departure'] >= row['scheduled_departure']:  

        return (row['departure'] -  \
            row['scheduled_departure']).seconds//60
    else:

        return -(row['scheduled_departure'] -  \
            row['departure']).seconds//60

def classify_flights(flights):
    '''
    classifies flights' : 
    a) destinations: 
    - int : international (1) vs domestic 0
    - city : city of the destination
    - name: name of the airline 
    b) delays:
    - delays: delayed (1) > 15 min vs not delayed (0)  
    - delay_min : nr of minutes the plane was delay 
    c) month 

    --------------------------------------------------
    flights: DataFrame 

    flight data 

    -------------------------------------------------

    returns : flight Dataframe  with additional 
    clasification columns 

    '''
    airports = get_dest_data(flights)

    logging.info(' Classifing the flights\' destinations ...')
    
    airlines = pd.read_csv('airlines.csv', header = 0,
             index_col = 0)

    flights['int'] = flights['destination'].map(
                    airports['Int'])
    flights['city'] = flights['destination'].map(
                    airports['City']).astype('category')
    flights['country'] = flights['destination'].map(
                       airports['Country']).astype('category')
    flights['name'] = flights['carrier'].map(airlines['name'])
    

    logging.info(' Classifing the flights\' delays ...')
    flights['delay_min'] = flights.apply(classify_delay,
                     axis = 1)
    flights['delay']= np.where(flights['delay_min']> 15, 1, 0)

    logging.info(' Classifing the flights by month...')
    flights['month'] = pd.DatetimeIndex(
                    flights['departure']).month.astype('category')
    
    return flights


