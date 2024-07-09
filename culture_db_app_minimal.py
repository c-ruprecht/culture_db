import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

# Initialize the Dash app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.css"
exp_btn_css = 'assets/exoort_btn.css'
app = dash.Dash()
#app = dash.Dash(__name__,
#                suppress_callback_exceptions=True,
#                prevent_initial_callbacks=True,
#                external_stylesheets=[dbc.themes.LUX, exp_btn_css, dbc_css])

# Simple layout for testing
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

# Run the server
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=True)
