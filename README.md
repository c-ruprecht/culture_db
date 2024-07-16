# Installation
cd /hpc/users/ruprec01/www/
git clone...

# create venv and install from requirements file
cd /hpc/users/ruprec01/www/culture_db
python3 -m venv /hpc/users/ruprec01/venv_culture_db # This path needs to be updated in index.wsgi
/hpc/users/ruprec01/venv_culture_db/bin/pip install -r requirements.txt

# test 
cd /hpc/users/ruprec01/www/culture_db
python3 culture_db_app.py

# access
git clone 

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

