import requests
import os
import json
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
USER = os.getenv("USER_DB")

# DB connection
mydb = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD
)

def fetch_weather_data(api_key, location_data):
    lat = location_data['lat']
    lon = location_data['lon']

    API_ENDPOINT = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,alerts,minutely&appid={api_key}"

    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        #logging.error(f"Error fetching weather data: {e}")
        return None

def fetch_current_id(connection, id_location):
    try:
        with connection.cursor(dictionary=True) as cursor:

            # Fetch the locations from DB with info
            sql = f"SELECT max(id_current) as id FROM weatherData.current WHERE id_location = {id_location};"
            cursor.execute(sql)
            data = cursor.fetchall()
            #logging.info("Location data fetched.")
            return(data[0]['id'])   
        
    except mysql.connector.Error as e:
        #logging.error(f"Error fetching location data: {e}")
        print(e)

def store_daily_pred_data(connection, weather_data, columns):
    try:
        with connection.cursor() as cursor:
            # Construct the SQL query dynamically based on the columns list
            columns_str = ', '.join(columns)
            placeholders_str = ', '.join(['%s'] * len(columns))
            
            sql = f"INSERT INTO weatherData.daily_pred ({columns_str}) VALUES ({placeholders_str})"
            
            # Extract the values for the specified columns from weather_data
            values = []
            for col in columns:
                if col.startswith('temp_'):
                    key = col.replace('temp_', '')
                    values.append(weather_data['temp'][key])
                elif col.startswith('feels_like_'):
                    key = col.replace('feels_like_', '')
                    values.append(weather_data['feels_like'][key])
                elif col.startswith('weather_'):
                    key = col.replace('weather_', '')
                    values.append(weather_data['weather'][0][key])
                else:
                    values.append(weather_data[col])
            
            cursor.execute(sql, values)
        connection.commit()
    except mysql.connector.Error as e:
        print(f"Error storing weather data: {e}")

location = {'lat': 49.1922443,'lon':16.6113382}
# Fetch location data
# weather_data = fetch_weather_data(API_KEY, location)
# Store location id
with open('weather_data.json', 'r') as openfile:
 
    # Reading from json file
    weather_data = json.load(openfile)

#print(weather_data['daily'][0])

columns = [
    'id_current', 'dt', 'sunrise', 'sunset',
    'temp_day', 'temp_min', 'temp_max', 'temp_night', 'temp_eve', 'temp_morn',
    'feels_like_day', 'feels_like_night', 'feels_like_eve', 'feels_like_morn',
    'pressure', 'humidity', 'dew_point', 'wind_speed', 'wind_deg',
    'weather_id', 'weather_main', 'weather_description', 'weather_icon',
    'clouds', 'pop', 'uvi'
]

pred_id = fetch_current_id(mydb, 33)

daily_pred = weather_data['daily']

for prediction in daily_pred:
    prediction['id_current'] = pred_id

    store_daily_pred_data(mydb, prediction, columns=columns)

#daily_pred['id_current'] = pred_id

#print(daily_pred)
