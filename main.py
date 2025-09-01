import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from models.location import *
from models.locationArea import *
from schemes import TrainerSchema    
from sqlalchemy.orm import Session
from models.trainer import *
from schemes.trainerSchema import *


app = FastAPI()
engine = create_engine('sqlite:///./test.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)

@app.get("/")
def home():
    return JSONResponse(content={"message": "This is the other service"})

@app.get("/randomLocation")
async def get_random_location():
    location = random.randint(1,10)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://pokeapi.co/api/v2/location/{location}")
        if response.status_code == 200:
            data = response.json()
            loc =  Location(**data)
            return JSONResponse(content=loc.model_dump_json())
        else:
            return JSONResponse(content={"error": "Location not found"}, status_code=404)

@app.get("/randomArea/{area_id}")
async def get_random_area(area_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://pokeapi.co/api/v2/location-area/{area_id}")
        if response.status_code == 200:
            data = response.json()
            loc =  LocationArea(**data)
            return JSONResponse(content=loc.pokemon_encounters[0].model_dump_json())
        else:
            return JSONResponse(content={"error": "Location not found"}, status_code=404)

@app.post("/createTrainer")
async def create_trainer(trainer: TrainerSchema):
    db = SessionLocal()
    close_db = True
    db_trainer = Trainer(**trainer.model_dump())
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    if close_db:
        db.close()
    return JSONResponse(content={"message": "Trainer created successfully", "trainer_id": db_trainer.name}, status_code=201)