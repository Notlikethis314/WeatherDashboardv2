# Weather Dash App

## Overview
This Weather Dash App provides real-time weather information, including temperature, humidity, pressure, for various czech cities.
I have created a MySQL server on linux VM, where I periodically store the weather data (that are available via OpenWeatherAPI)for several czech cities.
Afterwards, I query data for specific location inside the dash_app.py and visulize it inside the dashboard. Dashboard is beeing hosted on AWS EC2.

Currently, this project cannot be recreated, since all of the data are stored on unaccessable Database. I will write a How-to recreate MySQL DB in the future.

## Features
- Interactive dashboard displaying current, historical and predicted weather conditions.
- Real-time data updates.
- Visual representations of weather data through graphs.

## Technologies Used
- Python
- Dash
- Plotly
- Pandas
- Requests
- MySQL
- Linux
- AWS

## Installation
Currently cannot be replicated.

## Usage
Dashboard available on:
http://ec2-16-171-29-29.eu-north-1.compute.amazonaws.com:8050/