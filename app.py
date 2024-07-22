import dash
import dash_bootstrap_components as dbc
from navbar import CONTENT_STYLE
from dash.dependencies import Input, Output, State
from dash import callback, html, dcc
#from pages.layout import layout
from navbar import create_navbar


# For deployment, pass app.server (which is the actual flask app) to WSGI etc
# This allows to run the app locally via run_local.py and setting a correct pathname for the wsgi server

def create_app(prefix, db_path):
    app = dash.Dash(__name__,
                    external_stylesheets=[dbc.themes.BOOTSTRAP],
                    requests_pathname_prefix = prefix )
                    
    #Import all the pages               
    from pages import home, browse_sql, analysis_donor


    url_base = app.config.get('requests_pathname_prefix')
    app.layout = html.Div([create_navbar(url_base),
                        dcc.Location(id='url', refresh=False),
                        html.Div(id='page-content', style=CONTENT_STYLE),
                        dcc.Store(id='store-db-path', storage_type='local', data={'db_path': db_path})
                    ])
    #callback to manage content in the main page
    @callback(Output('page-content', 'children'),
                Input('url', 'pathname'))

    def display_page(pathname):        
        if pathname == url_base + 'home':
            return home.layout
        elif pathname == url_base + 'analysis_donor':
            return analysis_donor.layout
        elif pathname == url_base + 'browse_sql':
            return browse_sql.layout
        else:
            return home.layout
    return app





if __name__ == '__main__':
    app.run_server(debug=False)


    
