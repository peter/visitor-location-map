from datetime import datetime
import json
from src.db import db

TABLE_NAME = 'visitor_locations'
LIMIT = 1000

def row_to_doc(row):
    return { **row, 'location_info': json.loads(row['location_info']) }

def create_schema():
    db.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
            ip TEXT PRIMARY KEY,
            lat REAL,
            lng REAL,
            location_info TEXT,
            created_at TIMESTAMP
        )
    ''')
    db.execute(f'''
        CREATE INDEX IF NOT EXISTS {TABLE_NAME}_created_at_idx
        ON {TABLE_NAME}(created_at)
    ''')

def count():
    row = db.query_one(f'SELECT COUNT(*) count from {TABLE_NAME}')
    return row['count']

def get(ip):
    row = db.query_one(f'''
                SELECT *
                FROM {TABLE_NAME}
                WHERE ip = %s
            ''', (ip,))
    return row_to_doc(row) if row else None

def list():
    rows = db.query(f'''
                SELECT *
                FROM {TABLE_NAME}
                ORDER BY created_at DESC
                LIMIT %s
    ''', (LIMIT,))
    return [row_to_doc(row) for row in rows]

def create(ip, lat, lng, location_info):
    values = (ip, lat, lng, json.dumps(location_info), datetime.now())
    result = db.execute(f'''
                INSERT INTO {TABLE_NAME}
                (ip, lat, lng, location_info, created_at)
                VALUES (%s, %s, %s, %s, %s)
    ''', values)
    return result
