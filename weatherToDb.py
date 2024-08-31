import requests
import os
import json
from dotenv import load_dotenv
import mysql.connector
#import logging

# Setup logging
#logging.basicConfig(filename='weather_data.log', level=logging.INFO)

def store_current_weather(connection, current_weather_data, columns):
    try:
        with connection.cursor() as cursor:
            # Construct the SQL query dynamically based on the columns list
            columns_str = ', '.join(columns)
            placeholders_str = ', '.join(['%s'] * len(columns))
            
            sql = f"INSERT INTO weatherData.current ({columns_str}) VALUES ({placeholders_str})"
            
            # Extract the values for the specified columns from current_weather_data
            values = [current_weather_data['current'][col] for col in columns]
            
            cursor.execute(sql, values)
        connection.commit()
        #logging.info("Weather data stored successfully.")
    except mysql.connector.Error as e:
        #logging.error(f"Error storing weather data: {e}")
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

def store_hourly_pred_data(connection, weather_data, columns):
    try:
        with connection.cursor() as cursor:
            # Construct the SQL query dynamically based on the columns list
            columns_str = ', '.join(columns)
            placeholders_str = ', '.join(['%s'] * len(columns))
            
            sql = f"INSERT INTO weatherData.hourly_pred ({columns_str}) VALUES ({placeholders_str})"
            
            # Extract the values for the specified columns from weather_data
            values = []
            for col in columns:
                if col.startswith('weather_'):
                    key = col.replace('weather_', '')
                    values.append(weather_data['weather'][0][key])
                elif col == 'rain_1h':
                    # Handle the optional "rain" field
                    values.append(weather_data.get('rain', {}).get('1h', None))
                else:
                    values.append(weather_data[col])
            
            cursor.execute(sql, values)
        connection.commit()
        #print("Weather data stored successfully.")
    except mysql.connector.Error as e:
        print(f"Error storing weather data: {e}")

def fetch_locations_from_db(connection):
    try:
        with connection.cursor(dictionary=True) as cursor:
            # Fetch the locations from DB with info
            sql = "SELECT id, location_name, lat, lon FROM weatherData.locations"
            cursor.execute(sql)
            data = cursor.fetchall()
            #logging.info("Location data fetched.")
            return(data)   
        
    except mysql.connector.Error as e:
        #logging.error(f"Error fetching location data: {e}")
        print(e)

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

def fetch_weather_data(api_key, location_data):
    lat = location_data['lat']
    lon = location_data['lon']

    API_ENDPOINT = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=alerts,minutely&appid={api_key}"

    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        #logging.error(f"Error fetching weather data: {e}")
        print(e)
        return None


def main():
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

    columns = [
        'id_location',
        'dt',
        'sunrise',
        'sunset',
        'temp',
        'feels_like',
        'pressure',
        'humidity',
        'dew_point',
        'uvi',
        'clouds',
        'visibility',
        'wind_speed',
        'wind_deg'
    ]

    columns_daily_pred = [
        'id_current', 'dt', 'sunrise', 'sunset',
        'temp_day', 'temp_min', 'temp_max', 'temp_night', 'temp_eve', 'temp_morn',
        'feels_like_day', 'feels_like_night', 'feels_like_eve', 'feels_like_morn',
        'pressure', 'humidity', 'dew_point', 'wind_speed', 'wind_deg',
        'weather_id', 'weather_main', 'weather_description', 'weather_icon',
        'clouds', 'pop', 'uvi'
    ]

    columns_hourly_pred = [
        'id_current', 'dt', 'temp', 'feels_like', 'pressure', 'humidity', 'dew_point', 'uvi',
        'clouds', 'visibility', 'wind_speed', 'wind_deg', 'wind_gust',
        'weather_id', 'weather_main', 'weather_description', 'weather_icon',
        'pop', 'rain_1h'
    ]

    locations = fetch_locations_from_db(mydb)

    for location in locations:
        # Fetch location data
        weather_data = fetch_weather_data(API_KEY, location)
        # Store location id
        id_location = location['id']
        # Add location id
        weather_data['current']['id_location'] = id_location
        # Store current weather data into DB
        store_current_weather(mydb, weather_data, columns)
        # Fetch last id_current
        id_current = fetch_current_id(mydb, id_location)
        # Define daily pred data
        daily_pred = weather_data['daily']
        # Store daily pred data loop
        for daily_prediction in daily_pred:
            # Store id_current
            daily_prediction['id_current'] = id_current
            store_daily_pred_data(mydb, daily_prediction, columns=columns_daily_pred)

        hourly_pred = weather_data['hourly']
        for hourly_prediction in hourly_pred:
            # Store id_current
            hourly_prediction['id_current'] = id_current
            # Store hourly pred into DB
            store_hourly_pred_data(mydb, hourly_prediction, columns=columns_hourly_pred)


        
if __name__ == "__main__":
    main()