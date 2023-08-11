import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlalchemy as db

def lambda_handler(event, context):
    
    schema="wbs-project-3"
    host="wbs-project3-db.chofzj8c7a0m.eu-central-1.rds.amazonaws.com"
    user="admin"
    password= 'pBI2YY2mH6WnHLm0orcV' #api_keys.my_sql_password
    port=3306
    con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
    
    demographic_data = pd.DataFrame()
    cities = ['Lisbon']#, 'Berlin', 'Paris', 'Rome', 'London', 'Vienna', 'Athens', 'Copenhagen', 'Barcelona', 'Marseille', 'Munich', 'Warsaw', 'Prague']
    coordinates= []
    countries = []
    state = []
    population = []

 
    for city in cities:
        url = f'https://en.wikipedia.org/wiki/{city}'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            for e in soup.select('table.infobox tbody tr td'):
                if e.text.startswith('Coordinates: '):
                    coordinates.append(e.text.split('/')[-1].split(';'))
                    break

            country_found = False
            state_found = False
            population_found=False
            

            for e in soup.select('table.infobox tbody tr th'):
                if e.text == 'Country':
                    countries.append(e.find_next_sibling('td').get_text())
                    country_found = True
                    break

            for e in soup.select('table.infobox tbody tr th'):
                if e.text == 'State':
                    state.append(e.find_next_sibling('td').get_text())
                    state_found = True
                    break

            if not state_found:
                state.append('None')
                
            for e in soup.select('table.infobox tbody tr th'):
                if e.text.startswith('Population'):
                    for e in e.parent.find_next_siblings():
                        if 'Metro' in e.text:
                            population.append(e.select('td')[0].get_text())
                            population_found = True
                            break
            

            if not population_found:
                population.append('None')
                
    latitude = [coord[0] for coord in coordinates]
    longitude = [coord[1] for coord in coordinates]

    demographic_data = pd.DataFrame({'city': cities, 
                                 'state': state,
                                 'country' : countries,
                                 'population' : population,
                                 'longitude' : longitude,
                                 'latitude' : latitude})
    
    demographic_data['city_id'] = demographic_data.index
    demographic_data['population'] = demographic_data['population'].str.replace(r'(\[\d+\])', '', regex = True)
    demographic_data['population'] = demographic_data['population'].str.replace(r'\([^)]*\)', '', regex = True)
    demographic_data['country'] = demographic_data['country'].str.replace(r'(\[\w+\])', '', regex = True)
    demographic_data['population'] = demographic_data['population'].str.replace(r'\,', '', regex = True)
    
    demographic_data.to_sql('demographic_data',if_exists='append',con=con,index=False)


