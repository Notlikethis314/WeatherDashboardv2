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
from figures import *
from functions import *
                
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

# Define styles
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
                          'display': 'inline-block', 'margin-left': '10px'},
        'div_bounding_box':{'border-radius': '10px', 'background-color': '#e0e0e0',
                                            'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',
                                            'box-sizing': 'border-box',
                                            'margin-top':'10px', 'margin-right':'10px', 'margin-left':'10px'}
    }

# Query locations
locations = execute_query_create_df(cursor, sql_locations)

app = dash.Dash()

app.layout = html.Div( # Div with dropdown
    children=[
        html.Br(),
        html.H2('Please select a city: ', style={**styles['title_style']}),
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
                        # City overview DIV - Current weather, humidity and so on...
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
                                create_measure_section('humidity'),
                                
                                # Pressure section
                                create_measure_section('pressure'),

                                # Wind speed section
                                create_measure_section('wind_speed')

                            ], 
                            style={
                                'height': '400px', 
                                'width': '25%', 
                                **styles['div_bounding_box'], 'vertical-align': 'top', 'display':'inline-block',
                                'padding-right':'20px','padding-left':'20px', 'margin-top':'0px'}
                        ),
                        
                        # Prediction part
                        html.Div(
                            children=[
                                # Daily Prediction
                                html.Div(
                                    id='daily_prediction_blocks',
                                    style={
                                        'height': '40%',
                                        'background-color': '#fff',
                                        'display': 'flex',  # Keep the 5 inner divs in a row
                                        'justify-content': 'space-between'
                                    }
                                ),
                                # Hourly prediction
                                html.Div(
                                    html.Div(
                                        children=[
                                            dcc.Graph(id='hourly_pred_figure', animate=False, style={'height':'120%', 'width':'100%', 'overflow': 'hidden'})
                                        ],
                                        style={
                                            'height': 'calc(100% - 10px)', 
                                            'width': '100%', 
                                            **styles['div_bounding_box'], 'vertical-align': 'center', 'display':'block',
                                            'margin-top':'10px', 'margin-right':'10px', 'margin-left':'10px', 'overflow': 'hidden',
                                            'align-items': 'center', 'justify-content': 'center'
                                        }
                                    ),
                                    style={
                                        'height': '60%',
                                        'width':'100%',
                                })
                            ], 
                            style={
                                'height': '400px', 
                                'width': '75%', 
                                'display': 'inline-block', 
                            }
                        )
                    ], 
                    style={
                        'display': 'flex', 
                        'width': '100%', 
                        'height': '400px', 
                        'justify-content': 'space-between'  # Keeps both sections balanced
                    }
                ),
                
                # History charts div 
                create_div_for_history_fig(id='history_temp_fig'),
                create_div_for_history_fig(id='history_pressure_fig'),
                create_div_for_history_fig(id='history_humidity_fig')

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
    Output(component_id='daily_prediction_blocks', component_property='children'),
    Output(component_id='hourly_pred_figure', component_property='figure'),
    Output(component_id='history_temp_fig', component_property='figure'),
    Output(component_id='history_pressure_fig', component_property='figure'),
    Output(component_id='history_humidity_fig', component_property='figure'),
    Output(component_id='main_body', component_property='style'),
    Input(component_id='location_dd', component_property='value')
    
)

def update_history_chart(dd_value):
    current_info = []

    history_query = f'''
    SELECT 
        c.temp - 272.15 as TEMP,
        c.feels_like - 272.15 as TEMP_FEELS_LIKE,
        c.pressure as PRESSURE,
        c.humidity as HUMIDITY,
        c.wind_speed as WIND_SPEED,
        l.location_name,
        c.dt + (3600 * 2) as timestamp
    FROM weatherData.current c 
    JOIN weatherData.locations l ON (l.id = c.id_location)
    WHERE l.location_name = '{dd_value}';
    '''

    # Current tempreature data
    current_temp = execute_query_create_df(cursor, history_query)
    max_timestamp = current_temp['timestamp'].max() - (3600 * 2)

    daily_pred_query = f'''
    SELECT 
        DATE_FORMAT(FROM_UNIXTIME(dp.dt + (3600 * 2)), '%W') as day,
        DATE_FORMAT(FROM_UNIXTIME(dp.dt + (3600 * 2)), '%d/%m') as date,
        dp.temp_day - 272.15 as day_temp,
        dp.temp_night - 272.15 as night_temp,
        dp.weather_icon as picture,
        dp.weather_description as weather_desc,
        dp.clouds as cloudiness
    FROM weatherData.current c 
    JOIN weatherData.locations l ON (l.id = c.id_location)
    JOIN weatherData.daily_pred dp ON (dp.id_current = c.id_current)
    WHERE l.location_name = '{dd_value}' and c.dt = {max_timestamp};
    '''
    
    hourly_pred_query = f'''
    SELECT 
        hp.dt + (3600 * 2) as pred_timestamp,
        hp.temp - 272.15 as pred_temp,
        hp.feels_like - 272.15 as pred_feels_like,
        hp.clouds as clouds,
        hp.weather_description as weather_desc
    FROM weatherData.current c 
    JOIN weatherData.locations l ON (l.id = c.id_location)
    JOIN weatherData.hourly_pred hp ON (hp.id_current = c.id_current)
    WHERE l.location_name = '{dd_value}' and c.dt = {max_timestamp};
    '''

    # Daily prediction data
    daily_pred_data = execute_query_create_df(cursor, daily_pred_query)
    daily_pred_data = format_daily_pred_data(daily_pred_data)

    # Hourly prediction data
    hourly_pred_data = execute_query_create_df(cursor, hourly_pred_query)
    hourly_pred_data['pred_timestamp'] = pd.to_datetime(hourly_pred_data['pred_timestamp'], unit='s')

    # Current timestamp
    current_temp['timestamp'] = pd.to_datetime(current_temp['timestamp'], unit='s')
    last_timestamp = current_temp['timestamp'].max().strftime('%Y/%m/%d %H:%M')
    location_and_time = f"{dd_value}, {last_timestamp}"
    current_info.append(location_and_time)

    if dd_value:
        temp = current_temp[current_temp['location_name']==dd_value]

        # Current info block
        current_info.append(format_value(temp, 'TEMP', '°C'))
        current_info.append(format_value(temp, 'TEMP_FEELS_LIKE', '°C'))
        current_info.append(format_value(temp, 'HUMIDITY', ' %'))
        current_info.append(format_value(temp, 'PRESSURE', ' hPa'))
        current_info.append(format_value(temp, 'WIND_SPEED', ' m/s'))

        # Daily prediction blocks
        daily_pred_blocks = create_prediction_blocks(daily_pred_data.to_dict(orient='records'))
        current_info.append(daily_pred_blocks)

        # Hourly prediction graph
        fig_hourly_pred = create_fig_hourly_pred(hourly_pred_data)
        current_info.append(fig_hourly_pred)

        # History charts
        # Temp history
        fig_history_temp = create_fig_history_temp(temp)
        current_info.append(fig_history_temp)
        # Pressure history
        fig_history_pressure = create_fig_history_pressure(temp)
        current_info.append(fig_history_pressure)
        # Humidity history
        fig_history_humidity = create_fig_history_humidity(temp)
        current_info.append(fig_history_humidity)


        # Main body
        current_info.append({'display': 'block'})

    return current_info 
    
if __name__ == '__main__':
    app.run_server(debug=True)
