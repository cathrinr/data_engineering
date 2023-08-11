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
    password = os.environ['password_sql']
    port=3306
    con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
    
   
    query = "SELECT * FROM `wbs-project-3`.cities;"
    cities_df = pd.read_sql(query, con=con)
    
    weather_dict = {'city': [],
            'forecast_time': [],
            'outlook': [],
            'detailed_outlook': [],
            'temperature': [],
            'temperature_feels_like': [],
            'clouds': [],
            'rain': [],
            'snow': [],
            'wind_speed': [],
            'wind_deg': [],
            'humidity': [],
            'pressure': []}

    for index , row in cities_df.iterrows():
        open_weather_api_key = os.environ['open_weather_api_key']
        city = row['city_name']
        url = (f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_weather_api_key}&units=metric")
        response = requests.get(url)
        json = response.json()
    
        for i in json['list']:
            weather_dict['city'].append(json['city']['name'])
            weather_dict['forecast_time'].append(i['dt_txt'])
            weather_dict['outlook'].append(i['weather'][0]['main'])
            weather_dict['detailed_outlook'].append(i['weather'][0]['description'])
            weather_dict['temperature'].append(i['main']['temp'])
            weather_dict['temperature_feels_like'].append(i['main']['feels_like'])
            weather_dict['clouds'].append(i['clouds']['all'])
            try:
                weather_dict['rain'].append(i['rain']['3h'])
            except:
                weather_dict['rain'].append('0')
            try:
                weather_dict['snow'].append(i['snow']['3h'])
            except:
                weather_dict['snow'].append('0')
            weather_dict['wind_speed'].append(i['wind']['speed'])
            weather_dict['wind_deg'].append(i['wind']['deg'])
            weather_dict['humidity'].append(i['main']['humidity'])
            weather_dict['pressure'].append(i['main']['pressure'])
    weather_data = pd.DataFrame(weather_dict)
    
    city_ids = []
    for i, row in weather_data.iterrows():
        city_name = row['city']
        matching_city = cities_df[cities_df['city_name'].str.contains(city_name, case=False)]
        if not matching_city.empty:
            city_id = matching_city['city_id'].iloc[0]
            city_ids.append(city_id)
        else:
            city_ids.append(10000000000000) 
        
    weather_data['city_id'] = city_ids
    weather_data.to_sql('weather_automated',if_exists='append',con=con,index=False)