def day_prediction_block(dict_values):
    
    return html.Div(
        children=[
            # First div (Full height, half width)
            html.Div(
                children=[
                    html.H1(dict_values['day'],style={'font-size': '20px', 'color': '#333', 'font-family': 'Arial, sans-serif','margin-Top':'20px'}),
                    
                    html.Span(dict_values['day_temp'],style={'font-size': '48px', 'color': '#333', 'font-family': 'Arial, sans-serif','font-weight': 'bold'}),
                    html.Br(),
                    html.Br(),
                    html.Span(dict_values['night_temp'],style={'font-size': '28px', 'color': '#333', 'font-family': 'Arial, sans-serif'}),
                ],
                style={
                    'width': '50%',  # Half width
                    'height': '100%',  # Full height
                    'textAlign': 'center',
                    'box-sizing': 'border-box'
                }
            ),
            
            # Second div with two inner divs (each half height)
            html.Div(
                children=[
                    # Top half div
                    html.Div(
                        html.Img(src=f'https://openweathermap.org/img/wn/{dict_values['picture']}@2x.png', style={'width': '130px',  # Full width of second column
                            'height': '130px',}), 
                        style={
                            'width': '100%',  # Full width of second column
                            'height': '70%',  # Half height of column
                            'display': 'flex',  # Flexbox for centering
                            'align-items': 'center',  # Vertical centering
                            'justify-content': 'center',  # Horizontal centering                      
                            'box-sizing': 'border-box'
                        }
                    ),
                    # Bottom half div
                    html.Div(
                        children=[
                            html.Span('Chance of rain: ',style={'font-size': '12px', 'color': '#333', 'font-family': 'Arial, sans-serif'}),
                            html.Br(),
                            html.Span(dict_values['humidity'],style={'font-size': '20px', 'color': '#333', 'font-family': 'Arial, sans-serif'}),
                        ],
                        style={
                            'width': '100%',  # Full width of second column
                            'height': '30%',  # Half height of column
                            'textAlign': 'center',
                            'box-sizing': 'border-box'
                        }
                    )
                ], 
                style={
                    'width': '50%',  # Half width
                    'height': '100%',  # Full height
                    'box-sizing': 'border-box',
                    'display': 'flex',  # Flexbox for centering
                    'flex-direction': 'column'  # Stack the two divs vertically
                }
            )
        ],
        style={
            'width': '20%',  # Full width of this particular column
            'height': '100%',  # Full height of parent container
            'box-sizing': 'border-box',
            'display': 'flex',  # Use flexbox for the overall layout
            'flex-direction': 'row',  # Place the two divs side by side
            'border': 'solid 1px'
        }
    )