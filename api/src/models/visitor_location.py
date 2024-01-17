from datetime import datetime
import json
from src.database import execute, find_one, find_all

TABLE_NAME = 'visitor_locations'
LIMIT = 1000

def create_schema():
    execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
            ip TEXT PRIMARY KEY,
            lat REAL,
            lng REAL,
            location_info TEXT,
            created_at TIMESTAMP
        )
    ''')
    execute(f'''
        CREATE INDEX IF NOT EXISTS {TABLE_NAME}_created_at_idx
        ON {TABLE_NAME}(created_at)
    ''')

def get(ip):
    return find_one(f'''
                SELECT *
                FROM {TABLE_NAME}
                WHERE ip = ?
            ''', (ip,))

def list():
    return find_all(f'''
                SELECT *
                FROM {TABLE_NAME}
                ORDER BY created_at DESC
                LIMIT ?
    ''', (LIMIT,))

def create(ip, lat, lng, location_info):
    values = (ip, lat, lng, json.dumps(location_info), datetime.now())
    result = execute(f'''
                INSERT INTO {TABLE_NAME}
                (ip, lat, lng, location_info, created_at)
                VALUES (?, ?, ?, ?, ?)
    ''', values)
    return result
