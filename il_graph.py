import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 


def top_des (data, airport, color): 
    ''' draws and saves barchat of the
    top destinations for a given @airport

    ------------------------------------
    data : DataFrame 
    
    top destination data for the airport

    airport: str

    abbriviation for the airport of interest

    color: str

    color of the bars in the graph
    '''

    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(8, 6))
    width = 0.4 
    
    airports = data.loc[data['origin']== airport,
         'destination']
    y_pos = np.arange(len(airports))
    flights_count = data.loc[data['origin']==  \
                    airport, 'count']

    ax.barh(y_pos, flights_count, width, 
            align='center', color=color)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(airports, fontweight = 'bold',
                        fontsize=14)
    ax.invert_yaxis() 
    ax.set_xlabel('Total # of flights in 2014', 
                    fontsize=16)
    ax.set_title('Top 5 destinations from ' + airport, 
                fontsize=20)

    for i, v in enumerate(flights_count):
        ax.text(v - 900 , i, str(v), color='white', 
                fontweight = 'bold', fontsize=12)

    plt.tight_layout()
    plt.savefig(airport + '_dest.png')

    return None


def airlines_break_down (data, airport):
    ''' draws and saves piechat of % of 
    flights at the @airport by airline 

    ------------------------------------
    data : DataFrame 
    
    number of flights by each arline 

    airport: str

    abbriviation for the airport of interest

    '''
    fig, ax = plt.subplots(figsize = (7, 7), 
            subplot_kw=dict(aspect="equal"))

    
    top_5 = data.loc[data['origin']== airport].sort_values(
                'count', ascending=False).head(5) 

    

    rest = sum(data.loc[data['origin']== airport, 'count']) -  \
            sum(top_5['count'])  

    inx = top_5.index.max() 
    top_5 = top_5.append({'origin': airport, 'name': 'other',
                         'count': rest}, ignore_index = True)
    

    labels = top_5['name']
    sizes = top_5['count']
    

    wedges, texts, autotext = ax.pie(sizes, autopct = '%1.0f%%',  
                         pctdistance=0.55, startangle=90)
    
    ax.legend(wedges, labels, title = 'Airlines', loc = "best",
             fontsize = 12)
    
    plt.setp(autotext, size=14, weight="bold")
    
    ax.set_title("Flights by Airline : " + airport, fontsize = 22, 
                fontweight = 'bold')
    
    plt.tight_layout()

    plt.savefig(airport + '_arlines.png')
 

    return None



def monthly_delays(data, airport): 
        

        fig, ax1 = plt.subplots()
        
        ax2 = ax1.twinx()
        y1= data.loc['monthly_delays']
        y2= data.loc['total_delays']
        ax1.plot(data.columns, y1, color = 'g')
        ax2.plot(data.columns,y2, color = 'b')
        ax1.set_xlabel('months')
        
        ax1.set_ylabel('% delays', color='g')
        ax2.set_ylabel('total delays', color='b')
        ax1.set_title(" Monthly Delays : " + airport, fontsize = 20, 
                fontweight = 'bold')
        
        plt.show()
        
        return None 
