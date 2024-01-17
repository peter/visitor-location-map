from fastapi import FastAPI
import src.database as database
import src.models.visitor_location as visitor_location
import src.middleware.cors as cors_middleware
from src.routes import api_docs, health, visitor_locations

def init_database():
    database.connect()
    visitor_location.create_schema()

app = FastAPI(title="Visitor Location Map")

init_database()

cors_middleware.add(app)

app.include_router(api_docs.router)
app.include_router(health.router)
app.include_router(visitor_locations.router)
