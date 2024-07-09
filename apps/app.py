import dash
from dash import html, dcc
import plotly.express as px

app = dash.Dash(__name__)
server = app.server

# Sample layout
app.layout = html.Div([
    html.H1('My Dash App'),
    dcc.Graph(
        id='example-graph',
        figure=px.scatter(x=[1, 2, 3], y=[4, 1, 2])
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)