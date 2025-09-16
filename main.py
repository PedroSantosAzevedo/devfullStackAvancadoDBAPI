from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, Session
from models.pokemon import Pokemon  
from models.trainer import *
from schemes import *

app = FastAPI(title="Pokemon Database API", version="1.0.0")

# Database setup
engine = create_engine('sqlite:///./test.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.patch("/updatePlayerLocation/", tags=["trainers"])
async def update_player_location(playerLocationSchema: PlayerLocationSchema, db: Session = Depends(get_db)):
    trainer = db.query(Trainer).filter(Trainer.id == playerLocationSchema.trainer_id).first()
    if not trainer:
        raise HTTPException(status_code=404, detail="Player not found")
    
    trainer.current_location = playerLocationSchema.new_location
    db.commit()
    trainerSchema = TrainerSchema.model_validate(trainer)
    return JSONResponse(content=trainerSchema.model_dump(), status_code=200)

@app.post("/capturePokemon/", tags=["pokemon"])
async def capture_pokemon(capturePokemonSchema: CapturePokemonSchema, db: Session = Depends(get_db)):
    pokemon = PokemonSchema(**capturePokemonSchema.pokemon.model_dump())
    pokemonDB = Pokemon(**pokemon.model_dump(), trainer_id=capturePokemonSchema.trainer.id)

    trainer = db.query(Trainer).filter(Trainer.id == capturePokemonSchema.trainer.id).first()
    if not trainer:
        raise HTTPException(status_code=404, detail="Player not found")
    trainer.number_of_encounters += 1
    
    db.add(pokemonDB)
    db.commit()
    db.refresh(pokemonDB)
    
    return JSONResponse(content={"pokemon": pokemon.model_dump()}, status_code=200)

@app.get("/listPokemon/{trainer_id}", tags=["pokemon"])
async def list_pokemon(trainer_id: int, db: Session = Depends(get_db)):
    db_pokemon = db.query(Pokemon).filter(
        Pokemon.trainer_id == trainer_id
    ).all()
    
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="No Pokemon found for this trainer")
    
    pokemon_schemas = [PokemonSchema.model_validate(pokemon) for pokemon in db_pokemon]
    return JSONResponse(
        content={"pokemon": [pokemon.model_dump() for pokemon in pokemon_schemas]}, 
        status_code=200
    )

@app.post("/createTrainer", tags=["trainers"])
async def create_trainer(trainer: TrainerSchema, db: Session = Depends(get_db)):
    db_trainer = Trainer(**trainer.model_dump())
    
    if db_trainer is None:
        raise HTTPException(status_code=400, detail="Trainer data is required")
    
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    
    return JSONResponse(
        content={"message": "Trainer created successfully", "trainer_id": db_trainer.name}, 
        status_code=200
    )

@app.get("/getTrainer/{trainer_id}", tags=["trainers"])
async def get_trainer(trainer_id: int, db: Session = Depends(get_db)):
    trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()

    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    
    trainerSchema = TrainerSchema.model_validate(trainer)
    return JSONResponse(content=trainerSchema.model_dump(), status_code=200)

@app.delete("/deleteTrainer/{trainer_id}", tags=["trainers"])
async def delete_trainer(trainer_id: int, db: Session = Depends(get_db)):
    db_trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()
    
    if not db_trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    
    db.delete(db_trainer)
    db.commit()
    
    trainerSchema = TrainerSchema.model_validate(db_trainer)
    return JSONResponse(
        content={
            "message": "Trainer deleted successfully", 
            "trainer": trainerSchema.model_dump()
        }, 
        status_code=200
    )

@app.get("/listAllTrainers/", tags=["trainers"])
async def list_all_trainers(db: Session = Depends(get_db)):
    trainers = db.query(Trainer).all()
    
    if not trainers:
        raise HTTPException(status_code=404, detail="No trainers found")
    
    trainer_schemas = [TrainerSchema.model_validate(trainer) for trainer in trainers]
    return JSONResponse(
        content={"trainers": [trainer.model_dump() for trainer in trainer_schemas]}, 
        status_code=200
    )

@app.delete("/deletePokemon", tags=["pokemon"])
async def delete_pokemon(deleteInfo: DeletePokemonSchema, db: Session = Depends(get_db)):
    db_pokemon = db.query(Pokemon).filter(
        and_(
            Pokemon.id == deleteInfo.pokemon_id, 
            Pokemon.trainer_id == deleteInfo.trainer_id
        )
    ).first()
    
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    
    db.delete(db_pokemon)
    db.commit()
    
    pokemonScheme = PokemonSchema.model_validate(db_pokemon)
    return JSONResponse(
        content={
            "message": "Pokemon deleted successfully", 
            "pokemon": pokemonScheme.model_dump()
        }, 
        status_code=200
    )