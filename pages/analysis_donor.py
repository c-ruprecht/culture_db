import dash
from dash import html, dcc, dash_table, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
from sqlite3 import Error
import plotly.express as px
#from pages.layout import layout


dash.register_page(__name__, path = '/analysis_donor')


layout = html.Div(id = 'anal_donor')

@callback(
    Output('anal_donor', 'children'),
    Input('store-db-path', 'data')
)

def get_donors(store_data):

    db_path = store_data.get('db_path')
    #remove /app from path if it is present
    if db_path.startswith('/app/'):
        db_path = db_path[len('/app/'):]

    print('stored path '+ db_path)
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