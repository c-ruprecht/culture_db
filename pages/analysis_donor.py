import dash
from dash import html, dcc, dash_table, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
from sqlite3 import Error
import plotly.express as px
#from pages.layout import layout

db_path = "data/culture_db/culture.db"#layout['store-db-path'].data.get('db_path', '')

dash.register_page(__name__, path = '/analysis_donor')


layout = html.Div(id = 'anal_donor')

@callback(
    Output('anal_donor', 'children'),
    Input('store-db-path', 'data')
)

def get_donors(data):
    query = """select * from donor"""
    with sqlite3.connect(db_path) as connection:
        df = pd.read_sql_query(query, connection)
    
    fig = px.histogram(data_frame=df,
                    x = 'donor_species',
                    y='donor_id',
                    template = 'simple_white',
                    histfunc= 'count',
                    labels = {'donor_species': 'donor species'},
                    width = 800)
    
    children = [html.H1(children='Analysis donors'),
                              dcc.Graph(
                                id='donor_graph',
                                figure=fig
                            )
                        ]
    return children