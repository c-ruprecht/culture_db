import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
import sqlite3
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path='/home')

# Callback to get the database path from dcc.Store and update the content
@callback(
    [Output('donor_graph', 'figure'),
     Output('stats_summary', 'children')],
    [Input('url', 'pathname')],
    [State('store-db-path', 'data')]
)
def update_content(pathname, store_data):
    if not store_data:
        return dash.no_update, dash.no_update
    
    db_path = store_data.get('db_path')
    if db_path.startswith('/app/'):
        db_path = db_path[len('/app/'):]
    print('stored path '+ db_path)

    # Culture Library overview plot
    query = """SELECT * FROM library"""
    with sqlite3.connect(db_path) as connection:
        df = pd.read_sql_query(query, connection)
    df['date'] = pd.to_datetime(df['library_name'].apply(lambda x: x.split('_')[1]), format='%y%m%d')
    df = df.sort_values(['date', 'sample_id'], ascending=True)
    df['Culture Libraries'] = df.groupby('date')['library_name'].transform('count').cumsum()
    fig_cultlib = px.line(
        data_frame=df,
        x='date',
        y='Culture Libraries',
        template='simple_white',
        width=700
    )

    # General Statistics
    dict_general_stats = {}
    for table in ['donor', 'isolate', 'sample', 'library', 'archive', 'unique_strains', 'archive_species']:
        if table == 'archive':
            with sqlite3.connect(db_path) as connection:
                df_len = pd.read_sql_query(f"SELECT COUNT(*) FROM isolate WHERE archive_well IS NOT NULL", connection)
            dict_general_stats[table] = df_len.iloc[0].values[0]
        elif table == 'archive_species':
            qry = """SELECT COUNT(*) as total_count
                     FROM (SELECT DISTINCT genus, species FROM isolate
                           JOIN strain ON strain.strain_id = isolate.strain_id
                      ) as subquery;"""
            with sqlite3.connect(db_path) as connection:
                df_len = pd.read_sql_query(qry, connection)
            dict_general_stats[table] = df_len.iloc[0].values[0]
        elif table == 'unique_strains':
            qry = """SELECT COUNT(*) as total_count
                     FROM (
                        SELECT DISTINCT sample.donor_id, isolate.strain_id
                        FROM isolate
                        JOIN library ON library.library_id = isolate.library_id
                        JOIN sample ON library.sample_id = sample.sample_id
                        WHERE isolate.archive_well IS NOT NULL
                        GROUP BY sample.donor_id, isolate.strain_id
                    ) as subquery;"""
            with sqlite3.connect(db_path) as connection:
                df_len = pd.read_sql_query(qry, connection)
            dict_general_stats[table] = df_len.iloc[0].values[0]
        else:
            with sqlite3.connect(db_path) as connection:
                df_len = pd.read_sql_query(f"SELECT COUNT(*) FROM '{table}'", connection)
            dict_general_stats[table] = df_len.iloc[0].values[0]
    
    stats_summary = [
        html.P(f"{dict_general_stats.get('donor', 'N/A')} \t Total donors"),
        html.P(f"{dict_general_stats.get('sample', 'N/A')} \t Total samples processed"),
        html.P(f"{dict_general_stats.get('library', 'N/A')} \t Total culture libraries"),
        html.P(f"{dict_general_stats.get('isolate', 'N/A')} \t Total seed isolates"),
        html.P(f"{dict_general_stats.get('archive', 'N/A')} \t Archived isolates"),
        html.P(f"{dict_general_stats.get('archive_species', 'N/A')} \t Archived species"),
        html.P(f"{dict_general_stats.get('unique_strains', 'N/A')} \t Estimated unique archived strains")
    ]

    return fig_cultlib, stats_summary

# Layout definition
layout = html.Div(children=[
    html.H2(children='Documentation of mtc-db'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H3('General Information'),
                            dbc.Row([
                                dbc.Col(
                                    dcc.Graph(id='donor_graph'),
                                    width=5
                                ),
                                dbc.Col(
                                    html.Div(id='stats_summary'),
                                    width=5
                                ),
                            ])
                        ]
                    ),
                    className="mt-3",
                ),
                label="General Information"
            ),
            dbc.Tab(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H3('How to...'),
                            html.H5('... create analysis pipelines'),
                            html.P("", className="card-text"),
                        ]
                    ),
                    className="mt-3",
                ),
                label="How To's"
            ),
            dbc.Tab(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5('Release Notes v0'),
                            html.P("TO DO:", className="card-text"),
                            html.Ul([
                                html.Li("Everything"),
                            ]),
                        ]
                    ),
                    className="mt-3",
                ),
                label="Release Notes"
            )
        ]
    )
])
