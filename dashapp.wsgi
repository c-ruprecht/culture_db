import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/path/to/your/venv/lib/pythonX.X/site-packages')

# Add the directory containing your app.py to the Python path
sys.path.insert(0, '/hpc/users/ruprec01/www/culture_db/dashapp')

from app import server as application