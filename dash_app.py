import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import mysql.connector 
from dotenv import load_dotenv
import os
import numpy as np
import plotly.graph_objects as go

def create_label_value_list(input_list):
    return [{'label': item, 'value': item} for item in input_list]

load_dotenv()
# Variables
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
USER = os.getenv("USER_DB")

# DB connection
mydb = mysql.connector.connect(
  host=HOST,
  user=USER,
  password=PASSWORD
)

cursor = mydb.cursor()

sql = '''
SELECT 
	c.temp - 272.15 as TEMP,
    l.location_name,
    c.dt as timestamp,
    hp.temp - 272.15 as pred_TEMP,
    hp.dt as pred_timestamp
FROM weatherData.current c 
JOIN weatherData.locations l ON (l.id = c.id_location)
JOIN weatherData.hourly_pred hp ON (hp.id_current = c.id_current);
'''
cursor.execute(sql)

df_current = pd.DataFrame(cursor.fetchall())
df_current.columns = next(zip(*cursor.description))

df_current['timestamp'] = pd.to_datetime(df_current['timestamp'], unit='s')

app = dash.Dash()

app.layout = html.Div(
    children=[
        html.Br(),
        html.H2('Please select a city: '),
        dcc.Dropdown(id='location_dd',
            options=create_label_value_list(df_current['location_name'].unique().tolist()),
            style={'width': '200px'}
        ),
        html.Br(),
        dcc.Graph(id='history_line_chart')
    ]
)

@app.callback(
    Output(component_id='history_line_chart', component_property='figure'),
    Input(component_id='location_dd', component_property='value')
)

def update_history_chart(dd_value):
    temp = df_current.copy(deep=True)

    if dd_value:
        temp = temp[temp['location_name']==dd_value]
        fig_history_line_chart = px.line(temp, x='timestamp', y='TEMP')

    return fig_history_line_chart


if __name__ == '__main__':
    app.run_server(debug=True)
