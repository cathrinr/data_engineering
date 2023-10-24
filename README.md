# Data Engineering Project

This project is again a fictional case study. You have been hired as a Junior Data Engineer for a company that develops e-scooter sharing systems. They have noticed that it is of big interest to them to havint the scooters parked where users need them. Some requirements could be:
 - When it starts raining, more people use e-scooters.
 - In hilly areas, people use e-scooters to get up the hill but then walk down.
 - Tourists, that arrived with cheap flights, are a big potentioal group of users, but they mostly need the scooters neara touristic attractions.

Your task will now be to collect data about some of the most touristic cities in the world from external sources and store it appropriately so that in the future predictive models can be created. 

## Which tools to use?

### 1. Web Scraping data from Wikipedia
   With the use of Python library BeautifulSoup you can easily scrape all the needed data from Wikipedia. In this case this applied mainly to demographic data, like population, coordinates etc. If you want to read more about how to web scrape Wikipedia tables, check out my [Medium article](https://medium.com/@oboenfreak/web-scraping-wikipedia-tables-with-python-22223f761b1e) on this subject.
   
### 2. Collect data with API's
 In a next step you can collect more data from APIs, such as weather data or flight and airport data. In this project I used the following APIs:
 
### 3. Create database (MySQL)
   In order to store the data, we need to create a database. A first draft for the structue can be drawn by hand. This helps you to set up the database then correctly in MySQL and not mess up with connections and data types. The MySQL database needs then to be hosted in the cloud, so it can fetch all the data from the automated and static sources. 
   
### 4. Set up and automate a cloud pipeline (AWS)





