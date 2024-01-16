import time
from src.database import get_conn

def create_schema():
    get_conn().cursor().execute('''
        CREATE TABLE IF NOT EXISTS visitors(
            ip TEXT PRIMARY KEY,
            location TEXT,
            created_at TIMESTAMP
        )
    ''')

def create(ip, location):
    values = (ip, location, time.time())
    result = get_conn().cursor().execute('INSERT INTO visitors(ip, location, created_at) VALUES(?, ?, ?)', values)
    return result

def list():
    result = get_conn().cursor().execute('SELECT * from visitors')
    return result.fetchall()
