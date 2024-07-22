from dash import dcc, html
from navbar import CONTENT_STYLE, navbar
import os

#"/hpc/users/ruprec01/www/culture_db/data/culture_db/culture.db"
layout = html.Div([
        navbar,
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', style=CONTENT_STYLE),
        dcc.Store(id='store-db-path', storage_type='local', data={'db_path': "/hpc/users/ruprec01/www/culture_db/data/culture_db/culture.db"})
                                                            # data={'db_path': "data/culture_db/culture.db"})   
    ])
