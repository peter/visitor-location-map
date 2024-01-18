import psycopg2
import psycopg2.extras
import os
import re

DATABASE_NAME = 'visitor-location-map'
DATABASE_URL = os.environ.get('DATABASE_URL', f'postgresql://postgres:@localhost/{DATABASE_NAME}')

#############################################################
#
# Database Interface
#
#############################################################

def connect():
    global conn    
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True

def execute(sql, values = []):
    cur = conn.cursor()
    cur.execute(sql, values)
    return cur

def query(sql, values):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(sql, values)
    return list(map(dict, cur.fetchall()))

def query_one(sql, values):
    rows = query(sql, values)
    return rows[0] if len(rows) > 0 else None
