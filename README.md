# Database-driven web technology repository

To start the Python virtual environment:
```bash
# create the virtual environment
python3 -m venv .venv

# activate it (deactivate with "deactivate" command)
source .venv/bin/activate

# install dependencies
python3 -m pip install flask flask-sqlalchemy flask-login flask-wtf flask-httpauth Flask-Migrate

# ensure you have Sqlite3 installed
which sqlite3
# should output the executable path like /usr/bin/sqlite3
```