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

with open('data.json', 'w') as f:
    json.dump(response, f)