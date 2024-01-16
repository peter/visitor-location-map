from fastapi import FastAPI
import src.database as database
import src.models.visitor as visitor
import json

app = FastAPI()

database.connect()

visitor.create_schema()
location_info = {
  "status": "success",
  "country": "Sweden",
  "countryCode": "SE",
  "region": "AB",
  "regionName": "Stockholm County",
  "city": "Lidingö",
  "zip": "181 61",
  "lat": 59.3688,
  "lon": 18.118,
  "timezone": "Europe/Stockholm",
  "isp": "Telia Company AB",
  "org": "Telia Network Services",
  "as": "AS3301 Telia Company AB",
  "query": "90.230.167.205"
}

visitor.create('90.230.167.205', json.dumps(location_info))
print(visitor.list())

@app.get("/")
async def root():
    return {"message": "Hello World"}
