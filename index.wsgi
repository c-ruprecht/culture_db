import sys

#activate_this = '/hpc/users/ruprec01/venv_culture_db/bin/activate_this.py'

#exec(open(activate_this).read(), {'__file__': activate_this})

sys.path.insert(0,"/hpc/users/ruprec01/venv_culture_db/lib/python3.6/site-packages")


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