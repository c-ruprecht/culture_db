
import dash
from dash import html, Dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, callback, ctx
import dash_cytoscape as cyto
import pandas as pd
#from lims_tools import data_wrangler
from dash.dependencies import Input, Output, State
import sqlite3
from sqlite3 import Error
from components.layout import layout
import plotly.express as px

### Culture Library overview plot
query = """select * from library"""
db_path = layout['store-db-path'].data.get('db_path', '')
print(db_path)

with sqlite3.connect(db_path) as connection:
    print(connection)
    df = pd.read_sql_query(query, connection)
df['date'] = pd.to_datetime(df['library_name'].apply(lambda x: x.split('_')[1]), format='%y%m%d')
df = df.sort_values(['date', 'sample_id'], ascending = True)
df['Culture Libraries'] = df.groupby('date')['library_name'].transform('count').cumsum()
fig_cultlib = px.line(data_frame= df,
              x = 'date',
              y = 'Culture Libraries',
              template = 'simple_white',
              
              width =700)
### General Statistics 
dict_general_stats = {}
for table in ['donor', 'isolate', 'sample', 'library', 'archive', 'unique_strains','archive_species']:
    if table == 'archive':
        with sqlite3.connect(db_path) as connection:
            df_len = pd.read_sql_query(f"SELECT COUNT(*) FROM isolate WHERE archive_well IS NOT NULL", connection)
        dict_general_stats[table] = df_len.iloc[0].values[0]
    elif table == 'archive_species':
        qry = """ SELECT COUNT(*) as total_count
                  FROM (select distinct genus, species from isolate
                        join strain on strain.strain_id = isolate.strain_id
                ) as subquery;"""
        with sqlite3.connect(db_path) as connection:
            df_len = pd.read_sql_query(qry, connection)
        dict_general_stats[table] = df_len.iloc[0].values[0]
    elif table == 'unique_strains':
        qry = """ SELECT COUNT(*) as total_count
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
dict_general_stats

## Build app
app = Dash()

dash.register_page(__name__)


### Tabs and contents
tab_content = dbc.Card(
    dbc.CardBody(
        [   html.H3('General Information'),
            dbc.Row([
                dbc.Col(
                        dcc.Graph(id='donor_graph',
                                figure=fig_cultlib),
                        width = 5),
                dbc.Col([html.H5('Summary Statistics'),
                        html.P([f"{dict_general_stats['donor']} \t Total donors", html.Br(), #:<10 left aligns in field with space 10, needs to be combined with pre-wrap option
                                f"{dict_general_stats['sample']} \t Total samples processed", html.Br(),
                                f"{dict_general_stats['library']} \t Total culture libraries", html.Br(),
                                f"{dict_general_stats['isolate']} \t Total seed isolates", html.Br(),
                                f"{dict_general_stats['archive']} \t Archived isolates", html.Br(),
                                f"{dict_general_stats['archive_species']} \t Archived species", html.Br(),
                                f"{dict_general_stats['unique_strains']} \t Estimated unique archived strains", html.Br(), 
                                html.Br(),
                                ],
                                style={'white-space': 'pre'},#, 'font-family': 'monospace'},
                                className="card-text"),
                        html.P("""Unique strains are dereplicated by donor, meaning if donor 1 has 3 E. coli isolates archived they are counted as 1 unique isolate in the estimation""")
                        ],
                        width = 5),
                    ])
        ]
    ),
    className="mt-3",
)

tab_howtos = dbc.Card(
    dbc.CardBody(
        [   html.H3('How to...'),
            html.H5('... create analysis pipelines'),
            html.P("""
            """, className="card-text"),
            
        ]
    ),
    className="mt-3",
)

tab_releasenotes = dbc.Card(
    dbc.CardBody(
        [   html.H5('Release Notes v0'),
            html.P("TO DO:", className="card-text"),
            html.Ul([html.Li("""Everything"""),
                    ]),
            
        ]
    ),
    className="mt-3",
)



tabs = dbc.Tabs(
    [
        dbc.Tab(tab_content, label="General Information"),
        dbc.Tab(tab_howtos, label="How To's"),
        dbc.Tab(tab_releasenotes, label="Release Notes"),
    ]
)

layout = html.Div(children=[
                            html.H2(children='Documentation of mtc-db'),
                            tabs
                            ]
                )


