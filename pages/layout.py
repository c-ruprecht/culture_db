from dash import dcc, html

def store_db_path(path):
    layout = html.Div([dcc.Store(id='store-db-path', storage_type='local', data ={'db_path': path})]) 
    return layout
#"/hpc/users/ruprec01/www/culture_db/data/culture_db/culture.db"
#def create_layout(data_base_path = "/hpc/users/ruprec01/www/culture_db/data/culture_db/culture.db"):
#    layout = html.Div([
#            navbar,
#            dcc.Location(id='url', refresh=False),
#            html.Div(id='page-content', style=CONTENT_STYLE),
#            dcc.Store(id='store-db-path', storage_type='local', #data={'db_path': "/hpc/users/ruprec01/www/culture_db/data/culture_db/culture.db"})
#                                                                #data={'db_path': "data/culture_db/culture.db"},
#                                                                data = {'db_path': data_base_path})   
#        ])
#    return layout
