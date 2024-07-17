import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from navbar import navbar, CONTENT_STYLE

# For deployment, pass app.server (which is the actual flask app) to WSGI etc
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                requests_pathname_prefix='/culture_db/index.wsgi/',
                use_pages=True)

app.layout = html.Div([dash.page_container,
                        navbar,
                        dcc.Location(id='url', refresh=False),
                        html.Div(id='page-content', style=CONTENT_STYLE),
                        ])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname, db_path):
    if pathname == '/culture_db/':
        return home.layout
    elif pathname == '/culture_db/analysis_donor':
        return analysis_donor.layout
    elif pathname == '/culture_db/browse_sql':
        return second_test.layout
    else:
        return home.layout


if __name__ == '__main__':
    app.run_server(debug=True)
