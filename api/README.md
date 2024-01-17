# Visitor Location Map - REST API

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
curl http://localhost:8000/health
```

## Invoking the API with Curl

```sh
# The /visitor-locations stores the location of the request IP if it doesn't exist and lists all IPs (limit 1000)
curl -s http://localhost:8000/visitor-locations | jq
```

## Accessing the SQLite Database

```sh
sqlite3 sqlite-data/visitor-location-map.db
.schema visitor_locations
select * from visitor_location;
```
