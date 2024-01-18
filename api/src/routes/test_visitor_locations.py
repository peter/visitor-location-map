import os
import pytest
from fastapi.testclient import TestClient
import re

from src.main import app

client = TestClient(app)

def test_visitor_locations():
    os.environ['REQUEST_TEST_IP'] = '203.0.113.0'
    response = client.get("/visitor-locations")
    assert response.status_code == 200
    assert len(response.json()['locations']) == 1
    assert response.json()['locations'][0]['lat'] == 40.7127
    assert response.json()['locations'][0]['lng'] == -74.0059
    assert response.json()['locations'][0]['country'] == 'United States'
