import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, dcc, html
from navbar import CONTENT_STYLE, navbar
from apps import home, browse_sql, analysis_donor
from components.layout import layout

# Initialize the Dash app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.css"
exp_btn_css = 'assets/exoort_btn.css'
app = dash.Dash(suppress_callback_exceptions=True,
           prevent_initial_callbacks=True,
           external_stylesheets=[dbc.themes.LUX, exp_btn_css, dbc_css])

# Set the layout for the Dash app
app.layout = layout


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    State('store-db-path', 'data')
)
def display_page(pathname, db_path):
    if pathname == '/':
        return home.layout
    elif pathname == '/analysis_donor':
        return analysis_donor.layout
    elif pathname == '/browse_sql':
        return browse_sql.layout
    else:
        return home.layout

# Run the server
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=True)