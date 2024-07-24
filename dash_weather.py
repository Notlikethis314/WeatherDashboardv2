import plotly.express as px
import random
import pandas as pd

data = [
{
    "dt": 1684933200,
    "sunrise": 1684926650,
    "sunset": 1684977335,
    "temp": 292.04,
    "feels_like": 293.45,
    "pressure": 1016,
    "humidity": 90,
    "dew_point": 290.83,
    "uvi": 0.19,
    "clouds": 58,
    "visibility": 10900,
    "wind_speed": 3.49,
    "wind_deg": 97,
    "wind_gust": 7.39
},
{
    "dt": 1684936800,
    "sunrise": 1684926644,
    "sunset": 1684977333,
    "temp": 292.79,
    "feels_like": 292.92,
    "pressure": 1013,
    "humidity": 93,
    "dew_point": 291.34,
    "uvi": 0.17,
    "clouds": 60,
    "visibility": 10400,
    "wind_speed": 3.17,
    "wind_deg": 90,
    "wind_gust": 7.04
},
{
    "dt": 1684940400,
    "sunrise": 1684926643,
    "sunset": 1684977334,
    "temp": 291.99,
    "feels_like": 292.71,
    "pressure": 1017,
    "humidity": 85,
    "dew_point": 290.11,
    "uvi": 0.22,
    "clouds": 45,
    "visibility": 9600,
    "wind_speed": 3.01,
    "wind_deg": 91,
    "wind_gust": 6.53
},
{
    "dt": 1684944000,
    "sunrise": 1684926649,
    "sunset": 1684977337,
    "temp": 292.73,
    "feels_like": 293.41,
    "pressure": 1011,
    "humidity": 87,
    "dew_point": 291.19,
    "uvi": 0.25,
    "clouds": 62,
    "visibility": 9300,
    "wind_speed": 3.65,
    "wind_deg": 105,
    "wind_gust": 7.32
},
{
    "dt": 1684947600,
    "sunrise": 1684926651,
    "sunset": 1684977338,
    "temp": 292.81,
    "feels_like": 292.96,
    "pressure": 1012,
    "humidity": 91,
    "dew_point": 291.54,
    "uvi": 0.14,
    "clouds": 47,
    "visibility": 9800,
    "wind_speed": 2.88,
    "wind_deg": 89,
    "wind_gust": 6.12
},
{
    "dt": 1684951200,
    "sunrise": 1684926648,
    "sunset": 1684977331,
    "temp": 291.95,
    "feels_like": 292.13,
    "pressure": 1018,
    "humidity": 92,
    "dew_point": 290.75,
    "uvi": 0.20,
    "clouds": 65,
    "visibility": 10600,
    "wind_speed": 3.51,
    "wind_deg": 99,
    "wind_gust": 6.67
},
{
    "dt": 1684954800,
    "sunrise": 1684926640,
    "sunset": 1684977330,
    "temp": 292.15,
    "feels_like": 292.22,
    "pressure": 1015,
    "humidity": 86,
    "dew_point": 290.03,
    "uvi": 0.18,
    "clouds": 56,
    "visibility": 9400,
    "wind_speed": 3.22,
    "wind_deg": 92,
    "wind_gust": 6.87
},
{
    "dt": 1684958400,
    "sunrise": 1684926647,
    "sunset": 1684977329,
    "temp": 292.34,
    "feels_like": 293.01,
    "pressure": 1016,
    "humidity": 88,
    "dew_point": 290.58,
    "uvi": 0.12,
    "clouds": 49,
    "visibility": 10000,
    "wind_speed": 3.14,
    "wind_deg": 98,
    "wind_gust": 6.43
},
{
    "dt": 1684962000,
    "sunrise": 1684926642,
    "sunset": 1684977327,
    "temp": 292.42,
    "feels_like": 293.03,
    "pressure": 1014,
    "humidity": 84,
    "dew_point": 289.98,
    "uvi": 0.13,
    "clouds": 50,
    "visibility": 10800,
    "wind_speed": 3.43,
    "wind_deg": 103,
    "wind_gust": 7.15
},
{
    "dt": 1684965600,
    "sunrise": 1684926641,
    "sunset": 1684977336,
    "temp": 292.64,
    "feels_like": 293.21,
    "pressure": 1012,
    "humidity": 90,
    "dew_point": 290.67,
    "uvi": 0.24,
    "clouds": 60,
    "visibility": 9700,
    "wind_speed": 3.28,
    "wind_deg": 107,
    "wind_gust": 6.92
}]

df = pd.DataFrame(data)

# Convert 'dt' from UNIX timestamp to a readable datetime format
df['dt'] = pd.to_datetime(df['dt'], unit='s')



import plotly.graph_objects as go # or plotly.express as px
fig = px.line(df, x='dt', y='temp')

from dash import Dash, dcc, html

app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter