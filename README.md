git clone...
# Load module python 3.10
ml python/3.10.4
cd /hpc/users/ruprec01/www/culture_db
pip3 install --user -r requirements.txt

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

