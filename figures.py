import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def create_fig_hourly_pred(hourly_pred_data):
    temp_min = hourly_pred_data['pred_temp'].min() - 10
    temp_max = hourly_pred_data['pred_temp'].max() + 5


    fig_hourly_pred = px.area(
            hourly_pred_data, x='pred_timestamp', y='pred_temp', labels=dict(pred_timestamp='Time', pred_temp='Temperature (°C)'),
            line_shape='spline', color_discrete_sequence=px.colors.qualitative.Plotly[4:],  
        )
    # Customize hover template
    fig_hourly_pred.update_traces(hovertemplate='<b>Time: %{x|%Y-%m-%d %H:%M}</b><br>Temperature: %{y}<br>')
    fig_hourly_pred.update_traces(name='Temperature (°C)', showlegend=True)

    # Add custom data for hover (e.g., Feels_Like)
    fig_hourly_pred.update_traces(customdata=hourly_pred_data['pred_temp'].round(1))
    fig_hourly_pred.add_trace(
        go.Bar(
            x=hourly_pred_data['pred_timestamp'][::3],  # Plot every second hour
            y=hourly_pred_data['clouds'][::3] * (temp_max - temp_min) / 100,
            name='% of Clouds',
            hovertemplate='<b>Time: %{x|%Y-%m-%d %H:%M}</b><br>Clouds: %{customdata}%<extra></extra>',  # Show unscaled percentage
            customdata=hourly_pred_data['clouds'][::3],
            yaxis='y2',  # Use a secondary y-axis for the clouds percentage
            marker=dict(color='rgba(135,206,235,0.6)'),  # Light blue color for clouds
            width=1 * 3600 * 1000  # Adjust bar width
        )
    )
    
    for i in range(0, len(hourly_pred_data), 3):
        fig_hourly_pred.add_annotation(
            x=hourly_pred_data['pred_timestamp'][i],
            y=0,#(hourly_pred_data['clouds'][i]* (temp_max - temp_min) / 100)/2,  # Position above the bar
            text=hourly_pred_data['weather_desc'][i],  # The weather description
            showarrow=False,
            font=dict(size=10, color="black"),
            xanchor='center',
            yanchor='bottom',
            textangle=-30
            #yshift=-10
        )
    fig_hourly_pred.update_layout(
        yaxis=dict(
            title=None,
            range=[temp_min, temp_max],  # Set the range dynamically based on temperature values
            #tickvals=[i for i in range(int(temp_min), int(temp_max) + 1, 5)],
            ticksuffix='°C', showline=True,
            showgrid=True,  # Show gridlines
            gridcolor='white',  # Color of the gridlines
            gridwidth=0.5,  # Thickness of the gridlines
            griddash='dash'  # Make the gridlines dashed
    
        ),
        yaxis2=dict(
            #title='% of Clouds',
            overlaying='y',
            side='right',
            range=[0, (temp_max - temp_min) * 0.8],  # Scale cloud percentage to match the temperature range
            tickvals=[i * (temp_max - temp_min) / 100 for i in range(0, 101, 20)],  # Properly scaled ticks for cloud percentage
            ticktext=[f'{i}%' for i in range(0, 101, 20)],  # Cloud percentage is between 0 and 100
            showgrid=False  # Remove grid lines for secondary y-axis
        ),
        title='Prediction for next 48 Hours',
        title_font_family='Arial, sans-serif',
        plot_bgcolor='#e0e0e0',
        paper_bgcolor='#e0e0e0',
        barmode='overlay',  # Overlay the bars on the area plot
        xaxis_title='Time',
    )
    fig_hourly_pred.update_yaxes(autorange=True)
    return fig_hourly_pred

def create_fig_history_temp(data):
    fig = px.line(data, x='timestamp', y='TEMP', labels=dict(timestamp='Time', TEMP='Temperature (°C)'))

    fig.update_traces(name='Temperature (°C)', showlegend=True)

    fig.add_traces(
        go.Scatter(x=data['timestamp'], y=data['TEMP_FEELS_LIKE'], name='Feels like (°C)')
    )
    
    fig.update_layout(
        title='Recorded history of Temperature (°C)',
        title_font_family='Arial, sans-serif',
        yaxis=dict(
            ticksuffix='°C',
            showgrid=True,  # Show gridlines
            gridcolor='white',  # Color of the gridlines
            gridwidth=0.5,  # Thickness of the gridlines
            griddash='dash'  # Make the gridlines dashed
        ),
        plot_bgcolor='#e0e0e0',
        paper_bgcolor='#e0e0e0',
    )
    return fig

def create_fig_history_pressure(data):
    fig = px.line(data, x='timestamp', y='PRESSURE', labels=dict(timestamp='Time', PRESSURE='Pressure (hPa)'),
                  color_discrete_sequence=px.colors.qualitative.Plotly[3:])
    
    fig.update_traces(name='Pressure (hPa)', showlegend=True)

    fig.update_layout(
        title='Recorded history of Pressure (hPa)',
        title_font_family='Arial, sans-serif',
        yaxis=dict(
            ticksuffix=' hPa',
            showgrid=True,  # Show gridlines
            gridcolor='white',  # Color of the gridlines
            gridwidth=0.5,  # Thickness of the gridlines
            griddash='dash'  # Make the gridlines dashed
        ),
        plot_bgcolor='#e0e0e0',
        paper_bgcolor='#e0e0e0',
    )
    return fig

def create_fig_history_humidity(data):
    fig = px.line(data, x='timestamp', y='HUMIDITY', labels=dict(timestamp='Time', HUMIDITY='Humidity (%)'),
                  color_discrete_sequence=px.colors.qualitative.Plotly[2:])
    
    fig.update_traces(name='Humidity (%)', showlegend=True)

    fig.update_layout(
        title='Recorded history of Humidity (%)',
        title_font_family='Arial, sans-serif',
        yaxis=dict(
            ticksuffix='%',
            showgrid=True,  # Show gridlines
            gridcolor='white',  # Color of the gridlines
            gridwidth=0.5,  # Thickness of the gridlines
            griddash='dash'  # Make the gridlines dashed
        ),
        plot_bgcolor='#e0e0e0',
        paper_bgcolor='#e0e0e0',
    )
    return fig