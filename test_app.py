import dash
from dash import dcc, html

# for deployment, pass app.server (which is the actual flask app) to WSGI etc
app = dash.Dash()

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
# Run the server
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=True)