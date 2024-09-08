import plotly.express as px
import dash
import pandas as pd
import mysql.connector 
from dotenv import load_dotenv
import os
import numpy as np
import plotly.graph_objects as go

load_dotenv()
# Variables
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
USER = os.getenv("USER_DB")

# DB connection
mydb = mysql.connector.connect(
  host=HOST,
  user=USER,
  password=PASSWORD,
  database = "weatherData"
)

cursor = mydb.cursor()

sql = '''
SELECT 
	c.temp - 272.15 as TEMP,
    l.lat,
    l.lon,
    l.location_name,
    c.dt as timestamp
FROM current c 
JOIN locations l ON (l.id = c.id_location);
'''
cursor.execute(sql)

df_current = pd.DataFrame(cursor.fetchall())
df_current.columns = next(zip(*cursor.description))

df_current['timestamp'] = pd.to_datetime(df_current['timestamp'], unit='s') 

brno_data = df_current.loc[df_current['location_name']=='Brno']

fig = px.line(brno_data, x='timestamp', y='TEMP')
fig.show()
