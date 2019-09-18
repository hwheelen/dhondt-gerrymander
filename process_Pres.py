import pandas as pd
import geopandas as gpd
import numpy as np

#input starting path
start_path = ''
#load in congressional resuts from 1976-2018
raw_elec = gpd.read_file(start_path + 'GitHub/MEDSL/1976-2016-president.csv')
#load in congressional district county csv
dist_count = pd.read_csv(start_path + 'GitHub/dhondt-gerrymander/State_Congressional_District_Counts.csv')

#filter out years we don't care about
years = ['2012', '2016']
raw_elec = raw_elec[raw_elec['year'].isin(years)]

#for one state, aggregate votes for each major party
for year in years:
    elec = raw_elec.loc[raw_elec['year'] == year]
    party_dict = {}
    states = dist_count.state.unique()
    for st in states:
        print(st)
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
    
        for party, votes in st_party_df.iterrows():
            for i in range(1,num12+1):
                name = st + ' ' + year + ' ' + party + ', ' + 'bid ' + str(i)
                party_dict[name] = (st_party_df.loc[st_party_df.Party == party]['Party Votes'][0])/i
                
        party_df = pd.DataFrame.from_dict(data = party_dict, orient = 'index')
        #save csv
        party_df.to_csv(start_path + 'GitHub/dhondt-gerrymander/President/National_Party_Bids_Pres' + year +'.csv')
