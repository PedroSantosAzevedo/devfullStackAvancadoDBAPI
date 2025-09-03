import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from models.pokemon import Pokemon
from schemes.location import *
from schemes.locationArea import *
from schemes import TrainerSchema    
from sqlalchemy.orm import Session
from models.trainer import *
from schemes.pokemonSchema import PokemonSchema
from schemes.trainerSchema import *
import json

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
        
@app.get("/location/{locationName}")
async def get_location(locationName: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://pokeapi.co/api/v2/location/{locationName}")
        if response.status_code == 200:
            data = response.json()
            loc =  Location(**data)
            return JSONResponse(content={"location": loc.model_dump()}, status_code=200)
        else:
            return JSONResponse(content={"error": "Location not found"}, status_code=404)
        
@app.get("/randomArea/{location_name}")
async def get_random_area(location_name: str):
    async with httpx.AsyncClient() as client:
        location_response = await get_location(location_name)
        location_data = location_response.body.decode()
        
        location_dict = json.loads(location_data)["location"]
        location = Location(**location_dict)
        random_area = location.areas[random.randint(0, len(location.areas)-1)]
        response = await client.get(random_area.url)
        if response.status_code == 200:
            data = response.json()
            return JSONResponse(content=data)
        else:
            return JSONResponse(content={"error": "Location not found"}, status_code=404)     

@app.get("/getAreaRandomPokemon/{location_name}")
async def get_area_random_pokemon(location_name: str):
    async with httpx.AsyncClient() as client:
        area_response = await get_random_area(location_name)
        area_data = area_response.body.decode()
        area = LocationArea(**json.loads(area_data))
        randomEncounter = area.pokemon_encounters[random.randint(0, len(area.pokemon_encounters)-1)]
        response = await client.get(randomEncounter.pokemon.url)
        if response.status_code == 200:
            pokemon = PokemonSchema(**response.json())
            pokemonDB = Pokemon(**pokemon.model_dump(), trainer_name="Pedro")
            db = SessionLocal()
            db.add(pokemonDB)
            db.commit()
            db.refresh(pokemonDB)
            db.close()
            return JSONResponse(content=pokemon.model_dump_json())
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
    trainerScheme = TrainerSchema.model_validate(trainer)
    if trainer:
        return JSONResponse(trainerScheme.model_dump(), status_code=200)
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
        trainerScheme = TrainerSchema.model_validate(db_trainer)
        if close_db:
            db.close()
        return JSONResponse(content={"message": "Trainer deleted successfully", "trainer": trainerScheme.model_dump()}, status_code=200)
    else:
        if close_db:
            db.close()
        return JSONResponse(content={"error": "Trainer not found"}, status_code=404)
    
