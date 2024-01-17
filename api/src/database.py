import sqlite3
from contextlib import closing

# NOTE: we could have the db in memory as well with path ':memory:'
DATA_FILE_PATH = 'sqlite-data/visitor-location-map.db'

conn = None

# From https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_conn():
    return conn

def connect():
    global conn    
    conn = sqlite3.connect(DATA_FILE_PATH)
    conn.row_factory = dict_factory

def execute(*args, **kwargs):
    with closing(get_conn().cursor()) as cursor:
        result = cursor.execute(*args, **kwargs)
        get_conn().commit()
        return result

def find_one(*args, **kwargs):
    with closing(get_conn().cursor()) as cursor:
        result = cursor.execute(*args, **kwargs)
        return result.fetchone()

def find_all(*args, **kwargs):
    with closing(get_conn().cursor()) as cursor:
        result = cursor.execute(*args, **kwargs)
        return result.fetchall()
