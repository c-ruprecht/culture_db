import sys
import os

# Add the directory containing your app.py to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import server as application