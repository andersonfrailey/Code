import requests
import pandas as pd
import json
import argparse

# set up parser
parser = argparse.ArgumentParser()
parser.add_argument('station', help='WMATA station name')
args = parser.parse_args()

# read WMATA API key from file
api_file = open('/Users/andersonfrailey/apikeys.json', 'r')
api_keys = json.load(api_file)
api_file.close()

# read station keys
station_file = open('station_keys.json')
station_keys = json.load(station_file)
station_file.close()

# make request from WMATA and put data into a DataFrame
r_url = api_keys['wmata']['url']
params = {'api_key': api_keys['wmata']['key']}
trains = requests.get(r_url, params=params)
train_data = trains.json()

train_datadf = pd.DataFrame.from_dict(train_data['Trains'])
# find station key/value pair
try:
    station = station_keys[args.station.upper()]
except Exception as e:
    msg = ('Metro station "{}" not found.'.format(e.message) +
           ' Please check spelling')
    raise type(e)(msg)

# define results data frame
results_df = train_datadf[['Car', 'Line', 'DestinationName',
                           'Min']][train_datadf['LocationName'] == station]
results_df.columns = ['Cars', 'Line', 'Destination', 'Min']

print results_df.head()
