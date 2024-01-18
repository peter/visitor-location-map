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

## Deployment

Deployed to Heroku at [visitor-location-map-30ae10c6839e.herokuapp.com](https://visitor-location-map-30ae10c6839e.herokuapp.com/) in the EU region (AWS region eu-west-1 / Ireland):

```sh
export APP_NAME=visitor-location-map

# Create Heroku app
heroku apps:create --region eu $APP_NAME

# Add Postgres addon
heroku addons:create heroku-postgresql:mini -a $APP_NAME

# Make sure Postgres is used in production instead of SQLite
heroku config:set DATABASE=postgres -a $APP_NAME

# Deploy only the api-server sub directory to Heroku
git subtree push --prefix api heroku main

# Check API is up on Heroku
curl -s -i https://visitor-location-map-30ae10c6839e.herokuapp.com/health

# Various useful Heroku commands
heroku logs --tail -a $APP_NAME
heroku ps -a $APP_NAME
heroku pg:psql
heroku restart -a $APP_NAME
heroku info -a $APP_NAME
heroku config -a $APP_NAME
heroku labs:enable runtime-dyno-metadata -a $APP_NAME
heroku run printenv -a $APP_NAME
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
