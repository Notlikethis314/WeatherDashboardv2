import requests
import os
import json
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
USER = os.getenv("USER")

API_ENDPOINT = f"https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&exclude=hourly,alerts,minutely&appid={API_KEY}"
response = requests.get(API_ENDPOINT).json()

##

with open('data.json', 'w') as f:
    json.dump(response, f)

def store_current_weather(connection, current_weather_data):
    try:
        with connection.cursor() as cursor:
            sql = """INSERT INTO weather_data (location, temperature, humidity, wind_speed, timestamp)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                current_weather_data['current']['name'],
                current_weather_data['current']['temp_c'],
                current_weather_data['current']['humidity'],
                current_weather_data['current']['wind_kph']
            ))
        connection.commit()
        logging.info("Weather data stored successfully.")
    except pymysql.MySQLError as e:
        logging.error(f"Error storing weather data: {e}")