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
	avg(c.temp)-272.15 as avg_temp,
    l.lat,
    l.lon,
    l.location_name
FROM current c 
JOIN locations l ON (l.id = c.id_location)
group by l.location_name;
'''
cursor.execute(sql)

df_current = pd.DataFrame(cursor.fetchall())
df_current.columns = next(zip(*cursor.description))

fig = px.scatter_mapbox(df_current, lon="lon", lat='lat', 
                        color='avg_temp',
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        hover_name= 'location_name',
                        size='avg_temp')
fig.update_layout(
    mapbox_style='open-street-map', # Map style
    title="Temperature and Humidity ",  # Title of the map
    hovermode='closest',  # Hover mode for interactivity
    mapbox=dict(
        bearing=0, # Bearing of the map
        center=go.layout.mapbox.Center(
            lat=50.0874654, # Center latitude
            lon=14.4212535 # Center longitude
        ),
        pitch=0, # Map pitch
        zoom=7 # Initial map zoom level
    )
)
fig.show()

print(df_current)
