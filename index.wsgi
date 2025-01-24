import sys
import os

#Add correct python path to execute
#sys.path.insert(0,"/hpc/users/ruprec01/.local/lib/python3.10/site-packages")
# Add pytjon virtual environment
sys.path.insert(0, '/hpc/users/ruprec01/.local/lib/python3.10/site-packages/venv/lib/python3.10/site-packages')


# add your project directory to the sys.path
project_home = u'/hpc/users/ruprec01/www/culture_db'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# need to pass the flask app as "application" for WSGI to work
# for a dash app, that is at app.server
# see https://plot.ly/dash/deployment

from app import create_app
app = create_app(prefix = '/culture_db/index.wsgi/', db_path = '/hpc/users/ruprec01/www/culture_db/data/culture_db/culture.db')
application = app.server