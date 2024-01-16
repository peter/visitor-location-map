from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import src.database as database
import src.models.visitor as visitor
import json

app = FastAPI()

origins = [
    'http://localhost:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get('/health')
async def root():
    return {'status': 'ok'}

@app.get('/api/visitor-positions')
async def visitor_positions():
    return {'positions': [{'lat': 59.3688, 'lng': 18.118}]}
