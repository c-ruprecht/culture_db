import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from navbar import navbar, CONTENT_STYLE
from dash.dependencies import Input, Output, State
from dash import callback
from pages import home, browse_sql, analysis_donor


# For deployment, pass app.server (which is the actual flask app) to WSGI etc
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                requests_pathname_prefix='/culture_db/index.wsgi/')


app.layout = html.Div([navbar,
                        dcc.Location(id='url', refresh=False),
                        html.Div(id='page-content', style=CONTENT_STYLE),
                        dcc.Store(id='store-db-path', storage_type='local', data={'db_path': "data/culture_db/culture.db"})
                    ])



@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    State('store-db-path', 'data')
)
def display_page(pathname, db_path):
    if pathname == '/':
        return home.layout
    elif pathname == '/culture_db/index.wsgi/analysis_donor':
        return analysis_donor.layout
    elif pathname == '/culture_db/index.wsgi/browse_sql':
        return browse_sql.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)
