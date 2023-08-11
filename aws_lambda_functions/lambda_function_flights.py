import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlalchemy as db
import os


    
def lambda_handler(event, context):
    
    schema="wbs-project-3"
    host="wbs-project3-db.chofzj8c7a0m.eu-central-1.rds.amazonaws.com"
    user="admin"
    password= os.environ['password_sql']
    port=3306
    con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
    
    results = []
    
    query = "SELECT * FROM `wbs-project-3`.airports;"
    airports_df = pd.read_sql(query, con=con)
    
    for index, row in airports_df.iterrows():
        icao = row['icao_code']
        city = row['city']
        
        url = 'http://api.aviationstack.com/v1/flights'
        aviationstack_api_key = os.environ['aviationstack_api_key']
        
        params = {'access_key': {aviationstack_api_key}, 'arr_icao' : icao}
    
        response_aviationstack = requests.get(url, params=params).json()
        
        for i in range(len(response_aviationstack['data'])):
            output = {'city' : city,
                        'icaoCode' : icao,
                        'flight_date': response_aviationstack['data'][i]['flight_date'],
                        'departure_airport' :response_aviationstack['data'][i]['departure']['airport'],
                        'arrival_scheduled': response_aviationstack['data'][i]['arrival']['scheduled'],
                        'arrival_estimated': response_aviationstack['data'][i]['arrival']['estimated'],
                        'arrival_airport' : response_aviationstack['data'][i]['arrival']['airport'],
                        'airline' : response_aviationstack['data'][i]['airline']['name'],
                        'flightnumber_iata' : response_aviationstack['data'][i]['flight']['iata'],
                        }
                        
            results.append(output)
    
    flights_df = pd.DataFrame(results)
    
    flights_df['flight_id'] = flights_df.index
    flights_df.rename(columns = {'icaoCode' : 'icao_code'}, inplace = True)
    flights_df.to_sql('flights_automated',if_exists='append',con=con,index=False)

