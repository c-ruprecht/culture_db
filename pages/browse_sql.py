import dash
from dash import html, dcc, dash_table, callback
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
from sqlite3 import Error
#from pages.layout import layout


dash.register_page(__name__, path='/browse_sql')
db_path = "data/culture_db/culture.db"#layout['store-db-path'].data.get('db_path', '')

### Standard queries
queries = {
    'Everything archived': "select genus, species, strain, OD600_no_bkgnd, culture_type, culture_vessel, culture_name, bruker_name, bruker_score, library_name, health_status, archive_well, patient_id FROM growth gr, strain s, library l, culture c, isolate i, donor d, sample sa WHERE l.library_id=i.library_id AND s.strain_id=i.strain_id AND gr.culture_id=c.culture_id AND gr.isolate_id=i.isolate_id AND sa.sample_id=l.sample_id AND sa.donor_id = d.donor_id AND c.culture_type='archive';",
    'Everything with a genome': "select N50, length, genus, species, strain, OD600_no_bkgnd, culture_type, culture_vessel, culture_name, bruker_name, bruker_score, library_name, seed_well, archive_well, media_code, media_description, patient_id FROM genome g, growth gr, strain s, library l, culture c, isolate i, media m, donor d, sample sa WHERE g.isolate_id=i.isolate_id AND l.library_id=i.library_id AND s.strain_id=i.strain_id AND gr.culture_id=c.culture_id AND gr.isolate_id=i.isolate_id AND m.media_id=i.media_id AND sa.sample_id=l.sample_id AND sa.donor_id = d.donor_id;",
    # Add more predefined queries as needed
        }

@callback(
    Output('cytoscape', 'elements'),
    Input('store-db-path', 'data'),
    prevent_initial_call=False
)
def initialize_cytoscape(data):
    query = """
            SELECT 
                m.name AS table_name, 
                p.name AS column_name,
                p.type AS data_type
            FROM 
                sqlite_master m
            LEFT OUTER JOIN 
                pragma_table_info((m.name)) p
            WHERE 
                m.type = 'table'
            ORDER BY 
                m.name, 
                p.cid
            """

    try:
        with sqlite3.connect(db_path) as connection:
            df = pd.read_sql_query(query, connection)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []  # Return empty list in case of error

    li_elements = []
    unique_tables = df['table_name'].unique()

    # Create the table nodes
    li_elements.extend([
        {'data': {'id': f'node_{table}', 'table_name': table}}
        for table in unique_tables
    ])

    # Create connections if they exist
    for source_table in unique_tables:
        source_columns = set(df[df['table_name'] == source_table]['column_name'])
        
        for target_table in unique_tables:
            if target_table != source_table:
                target_columns = set(df[df['table_name'] == target_table]['column_name'])
                
                if source_columns.intersection(target_columns):
                    li_elements.append({
                        'data': {
                            'source': f'node_{source_table}',
                            'target': f'node_{target_table}'
                        }
                    })

    return li_elements

# Callback to update table based on node selection

@callback(
    Output('schema_tbl', 'columns'),
    Output('schema_tbl', 'data'),
    Input('store-db-path', 'data'),
    Input('cytoscape', 'selectedNodeData'),
    prevent_initial_call=False
)
def update_table(data, selected_nodes):
    query = """
            SELECT 
                m.name AS table_name, 
                p.name AS column_name,
                p.type AS data_type
            FROM 
                sqlite_master m
            LEFT OUTER JOIN 
                pragma_table_info((m.name)) p
            WHERE 
                m.type = 'table'
            ORDER BY 
                m.name, 
                p.cid
            """

    try:
        with sqlite3.connect(db_path) as connection:
            df = pd.read_sql_query(query, connection)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return [], []  # Return empty lists in case of error

    if not selected_nodes:
        filtered_df = df
        shared_columns = set()
    else:
        selected_tables = [node['table_name'] for node in selected_nodes if 'table_name' in node]
        filtered_df = df[df['table_name'].isin(selected_tables)]
        
        # Find shared columns
        if len(selected_tables) > 1:
            column_sets = [set(df[df['table_name'] == table]['column_name']) for table in selected_tables]
            shared_columns = set.intersection(*column_sets)
        else:
            shared_columns = set()

    # Function to format cell content for matching columns in tables
    def format_cell(row):
        if row['column_name'] in shared_columns:
            return f'<span style="font-size: 1.2em; font-weight: bold;">{row["column_name"]}</span>'
        else:
            return row['column_name']

    # Add formatted column
    filtered_df['formatted_column_name'] = filtered_df.apply(format_cell, axis=1)

    columns = [
        {'name': 'Table', 'id': 'table_name'},
        {'name': 'Column', 'id': 'formatted_column_name', 'presentation': 'markdown'},
        {'name': 'Data Type', 'id': 'data_type'}
    ]

    return columns, filtered_df.to_dict('records')

tab_query = html.Div([dcc.Dropdown([i for i in queries.keys()], id = 'dropdown-qry'),
                        dcc.Textarea(id='txt-area-sql',
                                    value='''select * from culture''',
                                    style={'width': '100%', 'height': 200}),
                        dbc.Button('Submit', id='sql-submit-button', n_clicks=0, color='dark', class_name="me-1"),
                        html.Div(id='sql-output', style={"padding": "5px"})
], className='dbc')

tab_schema = html.Div(children=[
    html.Div(dbc.Row([
                dbc.Col(cyto.Cytoscape(id='cytoscape',
                            layout={'name': 'circle'},#"random","preset","circle","concentric","grid","breadthfirst","cose","cose-bilkent","fcose","cola","euler","spread","dagre","klay"
                            style={'width': '100%', 'height': '750px'},
                            #zoom = 0.1,
                            stylesheet =[{ 'selector': 'node',
                                                'style': {
                                                    'label': 'data(table_name)'
                                                }
                                            },
                                            {'selector': '[table_name *= "tbl_sample_contents"]',
                                            'style': {
                                                'background-color': '#D62728',
                                                #'shape': 'rectangle'
                                            }}]               
                            ),width = 7),
                dbc.Col(dash_table.DataTable(id='schema_tbl',
                                            export_format="csv",
                                            filter_action='native',
                                            markdown_options={'html': True},
                                            cell_selectable=False,
                                            style_cell={'textAlign': 'left'},
                                            style_data={
                                                'whiteSpace': 'normal',
                                                'height': 'auto',
                                            },
                                                ), width = 5),
                    ]))]
                    )

tabs = dbc.Tabs([
                 dbc.Tab( tab_query, label = 'Query Database'),
                 dbc.Tab(tab_schema, label = 'Database Schema')])

layout = html.Div(children=[
                            html.H2(children='Browse Database'),
                            tabs
                            ]
                )


@callback(
    Output('sql-output', 'children'),
    Output('txt-area-sql', 'value'),
    Input('dropdown-qry', 'value'),
    Input('sql-submit-button', 'n_clicks'),
    State('txt-area-sql', 'value'),
    State('store-db-path', 'data')
)
def on_button_click(qry_drop, n_clicks, value, data):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'dropdown-qry':
        # Define your predefined queries here
        return dash.no_update, queries.get(qry_drop, '')

    elif triggered_id == 'sql-submit-button' and n_clicks > 0:
        try:
            with sqlite3.connect(db_path) as connection:
                df = pd.read_sql_query(str(value), connection)
            
            return dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.columns],
                filter_action='native',
                export_format="csv",
                style_as_list_view=True,
                style_header={'fontWeight': 'bold'},
                tooltip_data=[
                    {column: {'value': str(value), 'type': 'markdown'}
                     for column, value in row.items()} for row in df.to_dict('records')
                ],
                tooltip_header={i: i for i in df.columns},
                style_cell={
                    'padding': '5px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0,
                },
                tooltip_delay=0,
                tooltip_duration=None
            ), dash.no_update

        except Error as err:
            return html.Div(f"Error: {err}"), dash.no_update

    return html.Div("Click the submit button to execute the query"), dash.no_update

