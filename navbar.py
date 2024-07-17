"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""

#Usefull links for creatign page structure https://dash.plotly.com/urls
import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Input, Output, State,  dcc, html, Dash, callback

app = Dash()#external_stylesheets=[dbc.themes.BOOTSTRAP]

#Replace current sidebar with navbar from
#https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/


# the style arguments for the sidebar. We use position:fixed and a fixed width
NAVBAR_STYLE = {
    "position": "fixed",
    "top": "5rem",
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


search_bar = dbc.Row(
    [   dbc.Col(dbc.Button('Home', href = '/', class_name= 'btn btn-dark')),
        dbc.Col(dbc.DropdownMenu([
                                dbc.DropdownMenuItem('Donor', href = '/index.wsgi/analysis_donor'),
                                ],
                                label = 'Analysis',
                                color = 'dark',
                                )),
        dbc.Col(dbc.DropdownMenu([
                                dbc.DropdownMenuItem('Custom SQL Query', href = '/index.wsgi/browse_sql'),
                                ],
                                label = 'Browse',
                                color = 'dark',
                                )),
        
    ],
    class_name="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="right",
    #justify="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        #dbc.Col(html.Img(src=app.get_asset_url('logo_faithlab.png'), height="30px")),
                        dbc.Col(dbc.NavbarBrand("Microbial Culture DB", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                #href="https://plotly.com",
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
    dark=True, #True
)

# add callback for toggling the collapse on small screens
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