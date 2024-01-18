import os
import importlib

DATABASE = os.environ.get('DATABASE', 'sqlite')
db = importlib.import_module(f'src.db.{DATABASE}')
