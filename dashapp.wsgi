import sys

# Add the directory containing your app.py to the Python path
sys.path.insert(0, '/hpc/users/ruprec01/www/culture_db/dashapp')

from app import server as application