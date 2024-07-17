# Installation
cd /hpc/users/ruprec01/www/
git clone...
ml python/3.10.4
python3 -m venv /hpc/users/ruprec01/venv_culture_db
source /hpc/users/ruprec01/venv_culture_db/bin/activate
pip install -r requirements.txt


# create venv and install from requirements file
cd /hpc/users/ruprec01/www/culture_db
python3 -m venv /hpc/users/ruprec01/venv_culture_db # This path needs to be updated in index.wsgi
- activate environment
source /hpc/users/ruprec01/venv_culture_db/bin/activate
pip install -r requirements.txt
 - add activate this file to venv
 cd /hpc/users/ruprec01/www/culture_db
 cp activate_this.py /hpc/users/ruprec01/venv_culture_db/bin/

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

