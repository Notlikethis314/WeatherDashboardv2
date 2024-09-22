import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import mysql.connector
import pandas as pd

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

def create_label_value_list(input_list):
    return [{'label': item, 'value': item} for item in input_list]

def execute_query_create_df(cursor, query):
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

def format_value(data, column, suffix):
        value = data.sort_values('timestamp', ascending=False).iloc[0][column]
        return f"{value:.1f}{suffix}" if isinstance(value, (int, float)) else f"{value}{suffix}"

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

def create_div_for_history_fig(id):
    return html.Div(
                    dcc.Graph(id=id, style={'width':'100%', 'height':'100%', 'overflow': 'hidden'}), 
                    style={**styles['div_bounding_box'],'width':'100%', 'height':'400px', 'overflow': 'hidden'}
                )