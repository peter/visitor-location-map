import traceback
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
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

def location_lat_lng(location):
    return {'lat': location['lat'], 'lng': location['lng']}

@router.get('/visitor-locations')
async def visitor_locations(request: Request):
    request_ip = get_request_ip(request)
    # Check if we have the IP in the database
    location = visitor_location.get(request_ip)
    if location is None:
        # We have not seen the visitor IP before - lookup location and save it in the database
        location_info = fetch_location_from_ip(request_ip)
        lat = float(location_info['lat'])
        lng = float(location_info['lon'])
        visitor_location.create(request_ip, lat, lng, location_info)
    locations = visitor_location.list()
    locations_lat_lng = [location_lat_lng(location) for location in locations]
    return {'locations': locations_lat_lng}
