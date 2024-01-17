import time
import json
from src.database import get_conn

TABLE_NAME = 'visitor_locations'

def create_schema():
    get_conn().cursor().execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
            ip TEXT PRIMARY KEY,
            lat REAL,
            lng REAL,
            location_info TEXT,
            created_at TIMESTAMP
        )
    ''')

def get(ip):
    result = get_conn().cursor().execute(f'SELECT * FROM {TABLE_NAME} WHERE ip = ?', (ip,))
    return result.fetchone()

def list():
    result = get_conn().cursor().execute(f'SELECT * FROM {TABLE_NAME}')
    return result.fetchall()

def create(ip, lat, lng, location_info):
    values = (ip, lat, lng, json.dumps(location_info), time.time())
    result = get_conn().cursor().execute(f'INSERT INTO {TABLE_NAME}(ip, lat, lng, location_info, created_at) VALUES(?, ?, ?, ?, ?)', values)
    return result
