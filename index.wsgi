import os
import sys

# Set up the virtual environment
venv_path = '/hpc/users/ruprec01/venv_culture_db'
activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')

if os.path.exists(activate_this):
    exec(open(activate_this).read(), {'__file__': activate_this})
else:
    # Manual activation if activate_this.py doesn't exist
    old_os_path = os.environ.get('PATH', '')
    os.environ['PATH'] = os.path.join(venv_path, 'bin') + os.pathsep + old_os_path
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    site_packages = os.path.join(base, 'lib', 'python%s' % sys.version[:3], 'site-packages')
    prev_sys_path = list(sys.path)
    import site
    site.main()
    sys.path[:] = prev_sys_path + [site_packages]
    
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