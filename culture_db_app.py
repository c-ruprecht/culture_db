import dash
from dash import html, dcc
import plotly.express as px

app = dash.Dash()

# Sample data
df = px.data.iris()

# Create a simple layout
app.layout = html.Div([
    html.H1('Iris Dataset Dashboard'),
    dcc.Graph(
        id='scatter-plot',
        figure=px.scatter(df, x="sepal_width", y="sepal_length", color="species")
    )
])

# This is the server object that will be used by the WSGI file
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)