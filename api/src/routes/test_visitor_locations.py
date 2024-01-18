import os
import pytest
import re
from fastapi.testclient import TestClient
from src.main import app
import src.models.visitor_location as visitor_location

client = TestClient(app)

def test_visitor_locations():
    # Initial visit by first IP - creates new location in the database
    first_location = {
        'ip': '203.0.113.0',
        'lat': 40.7127,
        'lng': -74.0059,
        'country': 'United States'        
    }    
    count_before = visitor_location.count()
    os.environ['REQUEST_TEST_IP'] = first_location['ip']
    response = client.get("/visitor-locations")
    assert response.status_code == 200
    assert visitor_location.count() == count_before + 1
    assert len(response.json()['locations']) == 1
    assert response.json()['locations'][0]['lat'] == first_location['lat']
    assert response.json()['locations'][0]['lng'] == first_location['lng']
    assert response.json()['locations'][0]['country'] == first_location['country']

    # Repeat visit by first IP - does not create a new location in the database
    response = client.get("/visitor-locations")
    assert response.status_code == 200
    assert visitor_location.count() == count_before + 1
    assert len(response.json()['locations']) == 1
    assert response.json()['locations'][0]['lat'] == first_location['lat']
    assert response.json()['locations'][0]['lng'] == first_location['lng']
    assert response.json()['locations'][0]['country'] == first_location['country']

    # Initial visit by second IP - creates new location in the database (now there are two)
    second_location = {
        'ip': '94.191.136.112',
        'lat': 59.3915,
        'lng': 16.4223,
        'country': 'Sweden'        
    }    
    os.environ['REQUEST_TEST_IP'] = second_location['ip']
    response = client.get("/visitor-locations")
    assert response.status_code == 200
    assert visitor_location.count() == count_before + 2
    assert len(response.json()['locations']) == 2
    assert response.json()['locations'][0]['lat'] == second_location['lat']
    assert response.json()['locations'][0]['lng'] == second_location['lng']
    assert response.json()['locations'][0]['country'] == second_location['country']
    assert response.json()['locations'][1]['lat'] == first_location['lat']
    assert response.json()['locations'][1]['lng'] == first_location['lng']
    assert response.json()['locations'][1]['country'] == first_location['country']

    # Repeat visit by second IP - does not create a new location in the database
    response = client.get("/visitor-locations")
    assert response.status_code == 200
    assert visitor_location.count() == count_before + 2
    assert len(response.json()['locations']) == 2
