from dash import register_page, html

register_page(__name__, path='/analysis_donor')

layout = html.Div([
    html.H1('Donor Analysis'),
    html.P('This is the donor analysis page.')
])
