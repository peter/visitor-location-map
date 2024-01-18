import os
import sqlite3
from contextlib import closing

# NOTE: we could have the db in memory as well with path ':memory:'
SQLITE_DATA_PATH = os.environ.get('SQLITE_DATA_PATH', 'sqlite-data/visitor-location-map.db')

conn = None

# From https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# NOTE: this is a hack to allow using SQLite locally with SQL containing psycopg2 %s placeholders
def convert_placeholders(sql):
    return sql.replace('%s', '?')

#############################################################
#
# Database Interface
#
#############################################################

def connect():
    global conn
    conn = sqlite3.connect(SQLITE_DATA_PATH)
    conn.row_factory = dict_factory

def execute(sql, values = ()):
    with closing(conn.cursor()) as cursor:
        sqlite_sql = convert_placeholders(sql)
        result = cursor.execute(sqlite_sql, values)
        conn.commit()
        return result

def query(sql, values):
    with closing(conn.cursor()) as cursor:
        sqlite_sql = convert_placeholders(sql)
        result = cursor.execute(sqlite_sql, values)
        return result.fetchall()

def query_one(sql, values):
    with closing(conn.cursor()) as cursor:
        sqlite_sql = convert_placeholders(sql)
        result = cursor.execute(sqlite_sql, values)
        return result.fetchone()
