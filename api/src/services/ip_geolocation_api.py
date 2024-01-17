import requests

BASE_URL = 'http://ip-api.com/json'

def fetch_location_from_ip(ip):
    url = f'{BASE_URL}/{ip}'
    response = requests.get(url)
    data = response.json()
    return data
