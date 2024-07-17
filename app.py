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

app.layout = html.Div([html.H1('Multi-page app with Dash Pages'),
                        html.Div([
                            html.Div(
                                dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
                            ) for page in dash.page_registry.values()
                        ]),
                        dash.page_container
                    ])

#app.layout = html.Div([dash.page_container,
#                        navbar,
#                        dcc.Location(id='url', refresh=False),
#                        html.Div(id='page-content', style=CONTENT_STYLE),
#                        dcc.Store(id='store-db-path', storage_type='local', data={'db_path': "data/culture_db/culture.db"})])

if __name__ == "__main__":
    app.run_server(port=8050)
