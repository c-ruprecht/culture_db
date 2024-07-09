import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, dcc, html
from navbar import CONTENT_STYLE, navbar
from apps import home, browse_sql, analysis_donor
from components.layout import layout

# Initialize the Dash app
#dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.css"
#exp_btn_css = 'components/export_btn.css'

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.LUX],#, exp_btn_css, dbc_css],
                prevent_initial_callbacks=True,
                suppress_callback_exceptions=True)
# Set the layout for the Dash app
app.layout = layout

# Run the server
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=True)