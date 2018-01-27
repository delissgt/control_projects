import sys
sys.path.append('/var/www/nombreCarpeta/venv/app')
activate_this = '/var/www/nombreCarpeta/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
from app import app as application

