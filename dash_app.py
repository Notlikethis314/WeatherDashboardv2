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
    c.dt + 3600*2 as timestamp,
    hp.temp - 272.15 as pred_TEMP,
    hp.dt + 3600*2 as pred_timestamp
FROM weatherData.current c 
JOIN weatherData.locations l ON (l.id = c.id_location)
JOIN weatherData.hourly_pred hp ON (hp.id_current = c.id_current)
WHERE l.location_name IN ('Brno', 'Prague');
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
        html.Div(
            children=[
                # City Name + current time div
                html.Div(
                    children=[
                        # 
                        html.Div(
                            children=[
                                html.H3('Current temperature: '),
                                html.Br(),
                                html.H1(id='current_temp_H1')
                            ], style={'textAlign': 'center'}
                        ),
                        html.Div(
                            children=[
                                html.H5('Current humidity: ')
                            ]
                        )
                    ], style={'height':'400px', 'width':'25%', 'display':'inline-block','vertical-align':'top', 
                              #'border': '1px solid', 'background-image': 'linear-gradient(180deg, #fff, #ddd 40%, #ccc)',
                              #'box-shadow': '10px 5px 5px red'
                              'border': '1px solid'}
                ),
                # Prediction div
                html.Div(
                    children=[
                        html.H3('Test 2')
                    ], style={'height':'400px', 'width':'75%', 'border':'1px solid', 'display':'inline-block'}
                )
            ], style={'display': 'flex', 'width': '100%', 'height': '500px'}
        ),
        dcc.Graph(id='history_line_chart')
    ], style={'width':'100%'}
)

@app.callback(
    Output(component_id='history_line_chart', component_property='figure'),
    Output(component_id='current_temp_H1', component_property='children'),
    Input(component_id='location_dd', component_property='value')
    
)

def update_history_chart(dd_value):
    temp = df_current.copy(deep=True)

    if dd_value:
        temp = temp[temp['location_name']==dd_value]
        current_temp = temp.sort_values('timestamp', ascending=False).iloc[0]['TEMP']
        current_temp_formated = f"{current_temp:.1f}°C"

        fig_history_line_chart = px.line(temp, x='timestamp', y='TEMP')
    else:
        fig_history_line_chart=px.line()

    return fig_history_line_chart, current_temp_formated


if __name__ == '__main__':
    app.run_server(debug=True)
