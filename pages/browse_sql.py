import dash_html_components as html
from dash import register_page

register_page(__name__, path='/browse_sql')

layout = html.Div([
    html.H1('Custom SQL Query'),
    html.P('This is the custom SQL query page.')
])
