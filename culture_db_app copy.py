import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask

# for deployment, pass app.server (which is the actual flask app) to WSGI etc
app = dash.Dash()
#server = flask.Flask(__name__)

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
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'MontrÃ©al'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])