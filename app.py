import dash
import dash_bootstrap_components as dbc
from navbar import navbar, CONTENT_STYLE
from dash.dependencies import Input, Output, State
from dash import callback, html, dcc
from pages import home, browse_sql, analysis_donor
from pages.layout import layout

# For deployment, pass app.server (which is the actual flask app) to WSGI etc
# This allows to run the app locally via run_local.py and setting a correct pathname for the wsgi server

def create_app(prefix):
    app = dash.Dash(__name__,
                    external_stylesheets=[dbc.themes.BOOTSTRAP],
                    requests_pathname_prefix = prefix )

    app.layout = layout
    #callback to manage content in the main page
    @callback(Output('page-content', 'children'),
                Input('url', 'pathname'))

    def display_page(pathname):
        #url_base = app.config.get('requests_pathname_prefix', '/')
        url_base = app.config.get('requests_pathname_prefix')
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


    
