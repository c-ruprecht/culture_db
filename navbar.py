"""
This app creates a simple navbar layout using the dbc.Navbar component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plotly.com/urls
"""
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State, callback

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# The style arguments for the navbar
NAVBAR_STYLE = {
    "position": "fixed",
    "top": "0",
    "left": 0,
    "right": 0,
    "width": "100%",
    "padding": "0.5rem 1rem",
    "background-color": "#343a40",
}

# The styles for the main content position it below the navbar and add some padding
CONTENT_STYLE = {
    "margin-top": "4rem",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Button('Home', href='/', class_name='btn btn-dark')),
        dbc.Col(dbc.DropdownMenu([
            dbc.DropdownMenuItem('Donor', href='/analysis_donor'),
        ],
            label='Analysis',
            color='dark',
        )),
        dbc.Col(dbc.DropdownMenu([
            dbc.DropdownMenuItem('Custom SQL Query', href='/browse_sql'),
        ],
            label='Browse',
            color='dark',
        )),
    ],
    class_name="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="right",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Microbial Culture DB", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
)

# Add callback for toggling the collapse on small screens
@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run_server(port=8888)
