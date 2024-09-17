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



sql_locations = '''
SELECT DISTINCT
    l.location_name as location
FROM weatherData.locations l
'''

styles = {
        'title_style': {'font-family': 'Arial, sans-serif', 'color': '#333', 'padding': '10px'},
        'dropdown_style': {'width': '220px',
                'margin': '0px 0px 0px 0px', 
                'padding': '5px 20px 5px 5px', 
                'font-family': 'Arial, sans-serif', 
                'color': '#333'},
        'card_style': {'border-radius': '10px', 'background-color': '#f9f9f9',
                       'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'padding': '20px',
                       'box-sizing': 'border-box', 'vertical-align': 'top'},
        'text_measure_style': {'font-size': '16px', 'color': '#777', 'font-family': 'Arial, sans-serif', 
                          'display': 'inline-block'},
        'main_body_style': {'display': 'flex', 'width': '100%', 'padding': '0 20px', 'box-sizing': 'border-box', 
                            'justify-content': 'space-between'},
        'chart_style': {'margin-top': '20px', 'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 
                        'border-radius': '10px'},
        'content_measure_style':{'font-size': '16px', 'color': '#777', 'font-family': 'Arial, sans-serif', 
                          'display': 'inline-block', 'margin-left': '10px'}
    }

#cursor.execute(sql)

#df_current = pd.DataFrame(cursor.fetchall())
#df_current.columns = next(zip(*cursor.description))

#df_current['timestamp'] = pd.to_datetime(df_current['timestamp'], unit='s')

cursor.execute(sql_locations)
locations = pd.DataFrame(cursor.fetchall())
locations.columns = next(zip(*cursor.description))

app = dash.Dash()

app.layout = html.Div(
    children=[
        html.Br(),
        html.H2('Please select a city: ', style=styles['title_style']),
        dcc.Dropdown(
            id='location_dd',
            options=create_label_value_list(locations['location'].tolist()),
            placeholder="Select a city",  # No city is selected by default
            clearable=True,
            style=styles['dropdown_style']
        ),
        html.Br(),
        html.Div(
            # Graph body of dashboard
            children=[
                html.Div(
                    children=[
                        # City Name + current time div
                        html.Div(
                            children=[
                                # Current temperature and feels like div
                                html.Div(
                                    children=[
                                        html.H2(id='current_location', style={'color': '#555', 'font-family': 'Arial, sans-serif', 'margin-bottom': '10px'}),
                                        html.H3('Current temperature: ', style={'color': '#777', 'font-family': 'Arial, sans-serif', 'font-weight': 'normal'}),
                                        html.Div(
                                            children=[
                                                # Current temperature in large text
                                                html.Div(
                                                    html.H1(id='current_temp_H1',style={'font-size': '48px', 'color': '#333', 'font-family': 'Arial, sans-serif', 'margin-right': '20px'}), 
                                                    style={
                                                    'textAlign': 'center', 
                                                    'display': 'inline-block',
                                                    'margin-right': '5%',  # Adds space between temp and feels like
                                                    'margin-left': '20%'
                                                    }
                                                ),
                                                # Feels like temperature next to current temperature
                                                html.Div(
                                                    children=[
                                                        html.H4('Feels like: ', style={'color': '#777', 'font-family': 'Arial, sans-serif', 'font-weight': 'normal'}),
                                                        html.H3(id='current_feels_like', style={'font-size': '24px', 'color': '#333', 'font-family': 'Arial, sans-serif'})
                                                    ], 
                                                    style={
                                                        'textAlign': 'center',
                                                        'display': 'inline-block', 
                                                        'vertical-align': 'top'
                                                    }
                                                )
                                            ], style={'textAlign': 'center', 'display': 'flex'}
                                        )
                                    ], style={'textAlign': 'center', 'padding-bottom': '20px', 'align-items': 'center', 'justify-content': 'center'}
                                ),
                                
                                # Humidity section
                                html.Div(
                                    children=[
                                        html.Span('Current humidity: ', style=styles['text_measure_style']),
                                        html.Span(id='current_humidity', style=styles['content_measure_style'])
                                    ], style={'textAlign': 'center', 'padding-bottom': '10px'}
                                ),
                                
                                # Pressure section
                                html.Div(
                                    children=[
                                        html.Span('Current pressure: ', style=styles['text_measure_style']),
                                        html.Span(id='current_pressure', style=styles['content_measure_style'])
                                    ], style={'textAlign': 'center', 'padding-bottom': '10px'}
                                ),

                                # Wind speed section
                                html.Div(
                                    children=[
                                        html.Span('Current wind speed: ', style=styles['text_measure_style']),
                                        html.Span(id='current_wind_speed', style=styles['content_measure_style'])
                                    ], style={'textAlign': 'center', 'padding-bottom': '10px'}
                                )
                            ], 
                            style={
                                'height': '400px', 
                                'width': '25%', 
                                'border-radius': '10px', 'background-color': '#f9f9f9',
                       'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'padding': '20px',
                       'box-sizing': 'border-box', 'vertical-align': 'top', 'display':'inline-block'}
                        ),
                        
                        # Prediction div (Placeholder for now)
                        html.Div(
                            children=[
                                html.H3('Test 2', style={'font-family': 'Arial, sans-serif', 'color': '#555'})  # Replace with your prediction content
                            ], 
                            style={
                                'height': '400px', 
                                'width': '75%', 
                                
                                'display': 'inline-block', 
                                'border-radius': '10px', 
                                'background-color': '#fff',
                                'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 
                                'padding': '20px',
                                'box-sizing': 'border-box'
                            }
                        )
                    ], 
                    style={
                        'display': 'flex', 
                        'width': '100%', 
                        'height': '500px', 
                        'justify-content': 'space-between'  # Keeps both sections balanced
                    }
                ),
                
                # History chart div (hidden by default)
                html.Div(
                    dcc.Graph(id='history_line_chart'), 
                    id='history_line_container',
                    style=styles['chart_style']
                )
            ],id='main_body', style={'display': 'none'}
        )
    ], 
    style={'width': '100%', 'box-sizing': 'border-box'}
)

@app.callback(
    # Current text info
    Output(component_id='current_location', component_property='children'),
    Output(component_id='current_temp_H1', component_property='children'),
    Output(component_id='current_feels_like', component_property='children'),
    Output(component_id='current_humidity', component_property='children'),
    Output(component_id='current_pressure', component_property='children'),
    Output(component_id='current_wind_speed', component_property='children'),
    Output(component_id='history_line_chart', component_property='figure'),
    Output(component_id='main_body', component_property='style'),
    Input(component_id='location_dd', component_property='value')
    
)

def update_history_chart(dd_value):
    current_info = []

    sql = f'''
    SELECT 
        c.temp - 272.15 as TEMP,
        c.feels_like - 272.15 as TEMP_FEELS_LIKE,
        c.pressure as PRESSURE,
        c.humidity as HUMIDITY,
        c.wind_speed as WIND_SPEED,
        l.location_name,
        c.dt + 3600 * 2 as timestamp,
        hp.temp - 272.15 as pred_TEMP,
        hp.dt + 3600 * 2 as pred_timestamp
    FROM weatherData.current c 
    JOIN weatherData.locations l ON (l.id = c.id_location)
    JOIN weatherData.hourly_pred hp ON (hp.id_current = c.id_current)
    WHERE l.location_name = "{dd_value}"
    '''

    cursor.execute(sql)

    temp = pd.DataFrame(cursor.fetchall())
    temp.columns = next(zip(*cursor.description))
    temp['timestamp'] = pd.to_datetime(temp['timestamp'], unit='s')

    last_timestamp = temp['timestamp'].max().strftime('%Y/%m/%d %H:%M')

    location_and_time = f"{dd_value}, {last_timestamp}"
    current_info.append(location_and_time)

    if dd_value:
        temp = temp[temp['location_name']==dd_value]

        for column in ['TEMP', 'TEMP_FEELS_LIKE']:
            current_temp = temp.sort_values('timestamp', ascending=False).iloc[0][column]
            current_temp_formated = f"{current_temp:.1f}°C"
            # append current temp
            current_info.append(current_temp_formated)

        humidity = temp.sort_values('timestamp', ascending=False).iloc[0]['HUMIDITY']
        humidity = f"{humidity} %"
        current_info.append(humidity)

        pressure = temp.sort_values('timestamp', ascending=False).iloc[0]['PRESSURE']
        pressure = f"{pressure} hPa"
        current_info.append(pressure)

        wind_speed = temp.sort_values('timestamp', ascending=False).iloc[0]['WIND_SPEED']
        wind_speed = f"{wind_speed} km/h"
        current_info.append(wind_speed)

        fig_history_line_chart = px.line(temp, x='timestamp', y='TEMP', labels=dict(timestamp='Time', TEMP='Temperature'))
        
        current_info.append(fig_history_line_chart)
        current_info.append({'display': 'block'})

    return current_info 
    

    


if __name__ == '__main__':
    app.run_server(debug=True)
