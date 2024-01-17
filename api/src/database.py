import sqlite3

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
    # NOTE: we could have the db in memory as well with sqlite3.connect(":memory:")
    conn = sqlite3.connect('sqlite-data/visitor-location-map.db')
    conn.row_factory = dict_factory
