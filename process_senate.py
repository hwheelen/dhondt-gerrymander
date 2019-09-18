import pandas as pd
import geopandas as gpd
import numpy as np

#load in congressional resuts from 1976-2018
raw_elec = gpd.read_file('/Users/hwheelen/Documents/GitHub/MEDSL/1976-2018-house.csv')
#load in congressional district county csv
dist_count = pd.read_csv('/Users/hwheelen/Documents/GitHub/projects/DHondt/State_Congressional_District_Counts.csv')

#filter out years we don't care about
years = ['2010','2012', '2014', '2016', '2018']
raw_elec = raw_elec[raw_elec['year'].isin(years)]

#for one state, aggregate votes for each major party
states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
       'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
       'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
       'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
       'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
       'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
       'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
       'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
       'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
       'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
for year in years:
    elec = raw_elec.loc[raw_elec['year'] == year]
    party_dict = {}
    for st in states:
        num10 = dist_count.loc[dist_count.state == st]['2010'].values[0]
        num12 = dist_count.loc[dist_count.state == st]['2012'].values[0]
        state_df = pd.DataFrame()
        state_df = elec.loc[elec['state'] == st]
        state_df['votes'] = state_df['candidatevotes'].astype(str).astype(int)
        st_party_df = pd.pivot_table(state_df, index = ['party'], columns = ['state'], values = ['votes'], aggfunc = np.sum)
        st_party_df.columns = st_party_df.columns.to_series().str.join(' ')
        old_name = 'votes ' + st
        st_party_df['Party Votes'] = st_party_df[old_name].astype(str).astype(int)
        st_party_df = st_party_df[['Party Votes']]
        st_party_df['Party'] = st_party_df.index
        st_party_df = st_party_df[['Party','Party Votes']]
        if year == '2010':
            for party, votes in st_party_df.iterrows():
                for i in range(1,num10+1):
                    name = st + ' ' + year + ' ' + party + ', ' + 'bid ' + str(i)
                    party_dict[name] = (st_party_df.loc[st_party_df.Party == party]['Party Votes'][0])/i
                
                
        
        else:
            for party, votes in st_party_df.iterrows():
                for i in range(1,num12+1):
                    name = st + ' ' + year + ' ' + party + ', ' + 'bid ' + str(i)
                    party_dict[name] = (st_party_df.loc[st_party_df.Party == party]['Party Votes'][0])/i
                
        party_df = pd.DataFrame.from_dict(data = party_dict, orient = 'index')
        party_df.to_csv('/Users/hwheelen/Documents/GitHub/projects/DHondt/Congress/years/National_Party_Bids_' + year +'.csv')


state_party_dict = {
        'Alabama':['republican','democrat'],
        'Alaska':['republican','democrat'], 
        'Arizona':['republican','democrat'], 
        'Arkansas':['republican','democrat'], 
        'California':['republican','democrat'],
        'Colorado':['republican','democrat'],
        'Connecticut':['republican','democrat'], 
        'Delaware':['republican','democrat'], 
        'Florida':['republican','democrat'], 
        'Georgia':['republican','democrat'],
        'Hawaii':['republican','democrat'], 
        'Idaho':['republican','democrat'], 
        'Illinois':['republican','democrat'], 
        'Indiana':['republican','democrat'], 
        'Iowa':['republican','democrat'], 
        'Kansas':['republican','democrat'],
        'Kentucky':['republican','democrat'],
        'Louisiana':['republican','democrat'], 
        'Maine':['republican','democrat'],
        'Maryland':['republican','democrat'],
        'Massachusetts':['republican','democrat'],
        'Michigan':['republican','democrat'],
        'Minnesota':['republican','democrat'],
        'Mississippi':['republican','democrat'], 
        'Missouri':['republican','democrat'], 
        'Montana':['republican','democrat'],
        'Nebraska':['republican','democrat'], 
        'Nevada':['republican','democrat'], 
        'New Hampshire':['republican','democrat'], 
        'New Jersey':['republican','democrat'],
        'New Mexico':['republican','democrat'],
        'New York':['republican','democrat'],
        'North Carolina':['republican','democrat'], 
        'North Dakota':['republican','democrat'],
        'Ohio':['republican','democrat'],
        'Oklahoma':['republican','democrat'],
        'Oregon':['republican','democrat'], 
        'Pennsylvania':['republican','democrat'], 
        'Rhode Island':['republican','democrat'],
        'South Carolina':['republican','democrat'],
        'South Dakota':['republican','democrat'],
        'Tennessee':['republican','democrat'], 
        'Texas':['republican','democrat'],
        'Utah':['republican','democrat'], 
        'Vermont':['republican','democrat'],
        'Virginia':['republican','democrat'], 
        'Washington':['republican','democrat'], 
        'West Virginia':['republican','democrat'], 
        'Wisconsin':['republican','democrat'], 
        'Wyoming':['republican','democrat']}