import sys

#Add virtual environment to path
sys.path.insert(0,"/hpc/users/ruprec01/venv_culture_db/lib/python3.10/site-packages")

#Or use a local python installation
# ~/.local/lib/python3.7/site-packages

# add your project directory to the sys.path
project_home = u'/hpc/users/ruprec01/www/culture_db'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# need to pass the flask app as "application" for WSGI to work
# for a dash app, that is at app.server
# see https://plot.ly/dash/deployment

from app import app
application = app.server

app.config.update({
    'requests_pathname_prefix': '/culture_db/index.wsgi/'
})