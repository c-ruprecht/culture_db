# Installation
cd /hpc/users/ruprec01/www/
git clone https://github.com/c-ruprecht/culture_db.git
ml python/3.10.4
pip3 install --user --upgrade -r requirements.txt
export PYTHONPATH=~/.local/lib/3.10/site-packages/:$PYTHONPATH 
- you need to make sure that the index.wsgi file imports your specific paths like "/hpc/users/ruprec01/.local/lib/python3.10/site-packages"

# typing extension error
pip3 install --user --upgrade click flask importlib_metadata typing_extensions zipp plotly

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

