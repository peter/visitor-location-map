# visitor-location-map/api

REST API built with Python/FastAPI that serves locations based on IP for users of the web app. The location of users are stored in a SQLite database.

## Developer Setup

Dependencies:

* Python (built with 3.11)

```sh
# Setup virtual env and install dependencies
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt

# Start server
bin/start-dev 

# Ping server
curl http://localhost:8000
```

## Accessing the SQLite Database

```sh
sqlite3 visitor-location-map.db
.schema visitors
select * from visitors;
```