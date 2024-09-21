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

def execute_query_create_df(query):
    cursor.execute(query)
    temp = pd.DataFrame(cursor.fetchall())
    temp.columns = next(zip(*cursor.description))
    return temp

def format_daily_pred_data(daily_pred_data):
    daily_pred_data['day_temp'] = daily_pred_data['day_temp'].round(1).astype(str) + '°C'
    daily_pred_data['night_temp'] = daily_pred_data['night_temp'].round(1).astype(str) + '°C'
    daily_pred_data['cloudiness'] = daily_pred_data['cloudiness'].astype(str) + ' %'
    daily_pred_data['weather_desc'] = daily_pred_data['weather_desc'].str.capitalize()
    return daily_pred_data



# Function to create measurement section
def create_measure_section(measure):
    # Define the label and ID based on the measurement
    label_map = {
        'humidity': 'Current humidity: ',
        'pressure': 'Current pressure: ',
        'wind_speed': 'Current wind speed: '
    }
    
    id_map = {
        'humidity': 'current_humidity',
        'pressure': 'current_pressure',
        'wind_speed': 'current_wind_speed'
    }
    
    # Create the section dynamically based on the measure argument
    return html.Div(
        children=[
            html.Span(label_map.get(measure, ''), style=styles['text_measure_style']),
            html.Span(id=id_map.get(measure, ''), style=styles['content_measure_style'])
        ],
        style={'textAlign': 'center', 'padding-bottom': '10px'}
    )

 
def day_prediction_block(dict_values, width_of_block):
    '''
    Insert a dict in this format:
    {'day':'Monday', 
    'day_temp':'22°C', 
    'night_temp':'12°C', 
    'picture':'10d', 
    'cloudiness':'33 %'
    'weather_desc':'Clouds'}
    '''
    # Common styles
    text_style = {
        'font-family': 'Arial, sans-serif',
        'color': '#333'
    }
    centered_flex_style = {
        #'display': 'flex',
        #'align-items': 'center',
        #'justify-content': 'center',
        'box-sizing': 'border-box',
        'width': '100%'
    }

    return html.Div(
        children=[
            # Left column: day and temperatures
            html.Div(
                children=[
                    html.H1(dict_values.get('date', 'N/A'), style={**text_style, 'font-size': '15px', 'margin-top': '20px',}),
                    html.H1(dict_values.get('day', 'N/A'), style={**text_style, 'font-size': '15px',}),
                    html.Br(),
                    html.Span(dict_values.get('day_temp', 'N/A'), style={**text_style, 'font-size': '24px', 'font-weight': 'bold'}),
                    html.Br(),
                    html.Span(dict_values.get('night_temp', 'N/A'), style={**text_style, 'font-size': '18px'})
                ],
                style={
                    'width': '50%',
                    'height': '100%',
                    'text-align': 'center',
                    'box-sizing': 'border-box'
                }
            ),
            
            # Right column: image and rain chance/humidity
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Img(
                            src=f"https://openweathermap.org/img/wn/{dict_values.get('picture', '01d')}@2x.png",
                            style={'width': '90%', 'height': '100%'}
                        ),
                        html.Span(dict_values.get('weather_desc', 'N/A'), style={**text_style, 'font-size': '12px', 'position': 'relative', 'bottom': '25px'})
                        ],
                        style={**centered_flex_style, 'height': '50%', 'text-align': 'center'}
                    ),
                    html.Div(
                        children=[
                            html.Br(),
                            html.Span('Clouds : ', style={**text_style, 'font-size': '12px'}),
                            html.Br(),
                            html.Span(dict_values.get('cloudiness', 'N/A'), style={**text_style, 'font-size': '16px'})
                        ],
                        style={**centered_flex_style, 'height': '50%', 'text-align': 'center'}
                    )
                ],
                style={
                    'width': '50%',
                    'height': '100%',
                    'box-sizing': 'border-box',
                    'display': 'flex',
                    'flex-direction': 'column'
                }
            )
        ],
        style={
            'width': width_of_block,
            'height': '100%',
            'box-sizing': 'border-box',
            'display': 'flex',
            'flex-direction': 'row',
            'border-radius': '10px', 'background-color': '#e0e0e0',
            'box-shadow': '4px 4px 8px rgba(0, 0, 0, 0.1)', 'margin-left': '10px',
            'box-sizing': 'border-box'
        }
    )

def create_prediction_blocks(list_of_dicts, width_of_block='12.5%'):
    """
    """
    return [
        day_prediction_block(dict_values, width_of_block=width_of_block) 
        for dict_values in list_of_dicts
    ]

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

dict_values = {'day':'Monday', 'day_temp':'22°C', 'night_temp':'12°C', 'picture':'10d', 'cloudiness':'33 %'}

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
                                'border-radius': '10px', 'background-color': '#e0e0e0',
                                'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'padding': '20px',
                                'box-sizing': 'border-box', 'vertical-align': 'top', 'display':'inline-block',
                                'padding-right':'20px','padding-left':'20px'}
                        ),
                        
                        # Prediction part
                        html.Div(
                            children=[
                                html.Div(
                                    id='daily_prediction_blocks',
                                    style={
                                        'height': '40%',
                                        'background-color': '#fff',
                                        'display': 'flex',  # Keep the 5 inner divs in a row
                                        'justify-content': 'space-between'
                                    }
                                ),
                                html.Div(
                                    html.Div(
                                        id='hourly_prediction_block',
                                        children=[
                                            dcc.Graph(id='hourly_pred_figure', style={'height':'120%', 'width':'50%', 'overflow': 'hidden'})
                                        ],
                                        style={
                                            'height': 'calc(100% - 10px)', 
                                            'width': '100%', 
                                            'border-radius': '10px', 'background-color': '#e0e0e0',
                                            'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',
                                            'box-sizing': 'border-box', 'vertical-align': 'top', 'display':'block',
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
                                #'border-radius': '10px', 
                                #'background-color': '#fff',
                                #'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 
                                #'padding': '10px',
                                #'box-sizing': 'border-box'
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
    Output(component_id='daily_prediction_blocks', component_property='children'),
    Output(component_id='hourly_pred_figure', component_property='figure'),
    Output(component_id='history_line_chart', component_property='figure'),
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

    temp = execute_query_create_df(history_query)
    max_timestamp = temp['timestamp'].max() - (3600 * 2)

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
        hp.temp - 272.15 as pred_temp
    FROM weatherData.current c 
    JOIN weatherData.locations l ON (l.id = c.id_location)
    JOIN weatherData.hourly_pred hp ON (hp.id_current = c.id_current)
    WHERE l.location_name = '{dd_value}' and c.dt = {max_timestamp};
    '''

    daily_pred_data = execute_query_create_df(daily_pred_query)
    daily_pred_data = format_daily_pred_data(daily_pred_data)

    hourly_pred_data = execute_query_create_df(hourly_pred_query)
    hourly_pred_data['pred_timestamp'] = pd.to_datetime(hourly_pred_data['pred_timestamp'], unit='s')

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
        wind_speed = f"{wind_speed} m/s"
        current_info.append(wind_speed)

        # Daily prediction blocks
        daily_pred_blocks = create_prediction_blocks(daily_pred_data.to_dict(orient='records'))
        current_info.append(daily_pred_blocks)

        # Hourly prediction graph
        fig_hourly_pred = px.area(
            hourly_pred_data, x='pred_timestamp', y='pred_temp', labels=dict(pred_timestamp='Time', pred_temp='Temperature (°C)'),
            line_shape='spline'
        )
        fig_hourly_pred.update_layout(
            yaxis_title=None
        )
        fig_hourly_pred.update_yaxes(ticksuffix='°C')
        current_info.append(fig_hourly_pred)

        fig_history_line_chart = px.line(temp, x='timestamp', y='TEMP', labels=dict(timestamp='Time', TEMP='Temperature (°C)'))
        
        current_info.append(fig_history_line_chart)
        current_info.append({'display': 'block'})

    return current_info 
    

    


if __name__ == '__main__':
    app.run_server(debug=True)
