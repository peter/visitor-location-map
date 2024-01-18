# Visitor Location Map - REST API

REST API built with Python/FastAPI that serves locations based on IP for users of the web app. The location of users are stored in a SQLite database by default but the app also works on Postgres.

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

## Using Postgres instead of SQLite

To use Postgres instead of SQLite you need to have Postgres installed and running (i.e. use Postgres.app or Homebrew on Mac or use the [Postgres Docker image](https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/)):

```sh
# Create the Postgres database
createdb -U postgres visitor-location-map

# Start the server with Postgres
DATABASE=postgres bin/start-dev

# Connect with psql to check the database contents
psql -U postgres visitor-location-map
select * from visitor_locations
```

## Invoking the API with Curl

```sh
# The /visitor-locations stores the location of the request IP if it doesn't exist and lists all IPs (limit 1000)
curl -s http://localhost:8000/visitor-locations | jq
```

## Testing the Country Filter

If you start the server with the `TEST_LOCATIONS` you will get a few mock locations spread across the globe which is convenient for testing the country filter:

```sh
TEST_LOCATIONS=true bin/start-dev
```

## Accessing the SQLite Database

```sh
sqlite3 sqlite-data/visitor-location-map.db
.schema visitor_locations
select * from visitor_location;
```
