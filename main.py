import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from schemes.location import *
from schemes.locationArea import *
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
    return JSONResponse(content={"message": "Welcome to pokeServer by Pedro"})

@app.get("/randomLocation/{trainer_name}")
async def get_random_location(trainer_name: str):
    location = random.randint(1,10)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://pokeapi.co/api/v2/location/{location}")
        if response.status_code == 200:
            data = response.json()
            loc =  Location(**data)

            db = SessionLocal()
            trainer = db.query(Trainer).filter(Trainer.name == trainer_name).first()
            trainer.current_location = loc.name
            db.commit()
            trainerSchema = TrainerSchema.model_validate(trainer)
            db.close()
            return JSONResponse(content={"trainer": trainerSchema.model_dump()}, status_code=200)
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

@app.get("/getTrainer/{trainer_name}")
async def get_trainer(trainer_name: str):
    db = SessionLocal()
    close_db = True
    trainer = db.query(Trainer).filter(Trainer.name == trainer_name).first()
    if trainer:
        return JSONResponse("trainer", status_code=200)
    else:
        return JSONResponse(content={"error": "Trainer not found"}, status_code=404)

@app.delete("/deleteTrainer/{trainer_name}")
async def delete_trainer(trainer_name: str):
    db = SessionLocal()
    close_db = True
    db_trainer = db.query(Trainer).filter(Trainer.name == trainer_name).first()
    if db_trainer:
        db.delete(db_trainer)
        db.commit()
        if close_db:
            db.close()
        return JSONResponse(content={"message": "Trainer deleted successfully"}, status_code=200)
    else:
        if close_db:
            db.close()
        return JSONResponse(content={"error": "Trainer not found"}, status_code=404)
    
