# fastapi imports
from fastapi import FastAPI

# database  imports
from . import schemas, models
from .dbconfig import engine, SessionLocal
from sqlalchemy.orm import Session

# Creating the tables in the database based on the models in models.py file
models.Base.metadata.create_all(engine)

app = FastAPI()

# connection with database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# === GET ===

@app.get('/')
def index():
    return {'data':'hello world'}