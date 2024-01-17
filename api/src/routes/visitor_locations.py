import traceback
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import requests
import src.models.visitor_location as visitor_location
from src.services.ip_geolocation_api import fetch_location_from_ip

router = APIRouter()

def get_local_ip():
    url = 'https://api.ipify.org'
    response = requests.get(url)
    return response.text

def get_request_ip(request: Request):
    try:
        ip = request.client.host
        return get_local_ip() if ip == '127.0.0.1' else ip
    except Exception as error:
        print(f'Error thrown in get_request_ip', error, traceback.format_exc())
        return None

def response_location(location):
    return {
        'lat': location['lat'],
        'lng': location['lng'],
        'created_at': location['created_at']
    }

class Location(BaseModel):
    lat: float
    lng: float
    created_at: str
class VisitorLocationsResponseBody(BaseModel):
    locations: list[Location]

@router.get('/visitor-locations')
async def visitor_locations(request: Request) -> VisitorLocationsResponseBody:
    request_ip = get_request_ip(request)
    # Check if we have the IP in the database
    location = visitor_location.get(request_ip)
    print(f'location in db for request_ip={request_ip}: {location}')
    if location is None:
        # We have not seen the visitor IP before - lookup location and save it in the database
        location_info = fetch_location_from_ip(request_ip)
        lat = float(location_info['lat'])
        lng = float(location_info['lon'])
        visitor_location.create(request_ip, lat, lng, location_info)
    db_locations = visitor_location.list()
    locations = [response_location(location) for location in db_locations]
    return {'locations': locations}
