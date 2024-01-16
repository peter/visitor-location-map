import sqlite3

conn = None

def get_conn():
    return conn

def connect():
    global conn
    conn = sqlite3.connect('visitor-location-map.db')
