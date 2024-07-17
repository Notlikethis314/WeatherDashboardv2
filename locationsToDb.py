import requests
import os
import json
from dotenv import load_dotenv
import mysql.connector

cities = [
    "Prague",
    "Brno",
    "Ostrava",
    "Plzeň",
    "Liberec",
    "Olomouc",
    "České Budějovice",
    "Hradec Králové",
    "Pardubice",
    "Ústí nad Labem",
    "Zlín",
    "Havířov",
    "Kladno",
    "Most",
    "Opava",
    "Jihlava",
    "Frýdek-Místek",
    "Teplice",
    "Karviná",
    "Karlovy Vary",
    "Chomutov",
    "Děčín",
    "Mladá Boleslav",
    "Jablonec nad Nisou",
    "Prostějov",
    "Přerov",
    "Třinec"
]


# API
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

cursor = mydb.cursor()

#API_ENDPOINT = f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={API_KEY}"
API_ENDPOINT = f"http://api.openweathermap.org/geo/1.0/direct?q=Třinec&limit=5&appid={API_KEY}"
#API_ENDPOINT = f"https://api.openweathermap.org/data/3.0/onecall?lat={49.1922443}&lon={16.6113382}&appid={API_KEY}"

for city in cities:
    
    API_ENDPOINT = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_KEY}"
    response = requests.get(API_ENDPOINT).json()
    
    sql = """INSERT INTO weatherData.locations (location_name, lat, lon, country, region)
                 VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(sql, (
        response[0]['name'],
        response[0]['lat'],
        response[0]['lon'],
        response[0]['country'],
        response[0]['state']
    ))
    print(city)

mydb.commit()








