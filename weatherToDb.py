import requests
import os
import json
from dotenv import load_dotenv
import mysql.connector
import logging

# Setup logging
logging.basicConfig(filename='weather_data.log', level=logging.INFO)

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
        logging.info("Weather data stored successfully.")
    except mysql.connector.Error as e:
        logging.error(f"Error storing weather data: {e}")

def fetch_locations_from_db(connection):
    try:
        with connection.cursor(dictionary=True) as cursor:
            # Fetch the locations from DB with info
            sql = "SELECT id, location_name, lat, lon FROM weatherData.locations"
            cursor.execute(sql)
            data = cursor.fetchall()
            return(data)
        logging.info("Location data fetched.")
    except mysql.connector.Error as e:
        logging.error(f"Error fetching location data: {e}")

def fetch_weather_data(api_key, location_data):
    lat = location_data['lat']
    lon = location_data['lon']

    API_ENDPOINT = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,alerts,minutely&appid={api_key}"

    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return None


def main():
    load_dotenv()

    API_KEY = os.getenv("API_KEY")
    PASSWORD = os.getenv("PASSWORD")
    HOST = os.getenv("HOST")
    USER = os.getenv("USER")

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
        
if __name__ == "__main__":
    main()