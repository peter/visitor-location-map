import os
import traceback
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import requests
import src.models.visitor_location as visitor_location
from src.services.ip_geolocation_api import fetch_location_from_ip

router = APIRouter()

TEST_LOCATIONS = [
    {'lat': 59.3688, 'lng': 18.118, 'country': 'Sweden', 'created_at': '2024-01-17 13:36:15.563035'}, # home
    {'lat': 40.712776, 'lng': -74.005974, 'country': 'United States', 'created_at': '2024-01-17 13:36:15.563035'}, # NYC
    {'lat': 48.856613, 'lng': 2.352222, 'country': 'France', 'created_at': '2024-01-17 13:36:15.563035'}, # Paris
    {'lat': 34.052235, 'lng': -118.243683, 'country': 'United States', 'created_at': '2024-01-17 13:36:15.563035'}, # Log Angeles
    {'lat': 22.396427, 'lng': 114.109497, 'country': 'China', 'created_at': '2024-01-17 13:36:15.563035'} # Hong Kong
]

def get_local_ip():
    url = 'https://api.ipify.org'
    response = requests.get(url)
    return response.text

def get_request_ip(request: Request):
    try:
        if os.environ.get('REQUEST_TEST_IP'):
            return os.environ.get('REQUEST_TEST_IP')
        ip = request.client.host
        return get_local_ip() if ip == '127.0.0.1' else ip
    except Exception as error:
        print(f'Error thrown in get_request_ip', error, traceback.format_exc())
        return None

def response_location(location):
    return {
        'lat': location['lat'],
        'lng': location['lng'],
        'country': location['location_info']['country'],
        'created_at': str(location['created_at'])
    }

class Location(BaseModel):
    lat: float
    lng: float
    country: str
    created_at: str
class VisitorLocationsResponseBody(BaseModel):
    locations: list[Location]

@router.get('/visitor-locations')
async def visitor_locations(request: Request) -> VisitorLocationsResponseBody:
    request_ip = get_request_ip(request)
    # Check if we have the IP in the database
    location = visitor_location.get(request_ip)
    print(f'DEBUG: location in db for request_ip={request_ip}: {location}')
    if location is None:
        # We have not seen the visitor IP before - lookup location and save it in the database
        location_info = fetch_location_from_ip(request_ip)
        lat = float(location_info['lat'])
        lng = float(location_info['lon'])
        visitor_location.create(request_ip, lat, lng, location_info)
    if os.environ.get('TEST_LOCATIONS'):
        locations = TEST_LOCATIONS
    else:
        db_locations = visitor_location.list()
        locations = [response_location(location) for location in db_locations]
    return {'locations': locations}
