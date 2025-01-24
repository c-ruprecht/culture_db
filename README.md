# Installation on minerva
cd /hpc/users/ruprec01/www/
ml git
git clone https://github.com/c-ruprecht/culture_db.git
ml python/3.10.4
pip3 install --user --upgrade -r requirements.txt
pip3 install --user -r requirements.txt

export PYTHONPATH=~/.local/lib/3.10/site-packages/:$PYTHONPATH 
- you need to make sure that the index.wsgi file imports your specific paths like "/hpc/users/ruprec01/.local/lib/python3.10/site-packages"

# updating
ml git
cd /hpc/users/ruprec01/www/culture_db
git pull

# typing extension error
pip3 install --user --upgrade click flask importlib_metadata typing_extensions zipp plotly

# Running local
## Create virtual environment to run
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python3 run_local.py
## actually run the db
- the prefix for index.wsgi to be called is added by the create_app() function defined in app.py
- this allows to run the dashboard for debugging locally first using run_local.py that uses '/' as path prefix
git clone ...
cd to_target_folder/
source .venv/bin/activate
python3 run_local.py

# update
cd /hpc/users/ruprec01/www/culture_db
git pull

# Git error 
git reset --hard origin/main

# Accessing error logs
ssh ruprec01@minerva.hpc.mssm.edu
ssh ruprec01@web01
cd /var/log/httpd/uhpc
cat ruprec01.u.hpc.mssm.edu.error

