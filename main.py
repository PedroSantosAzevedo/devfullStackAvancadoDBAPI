from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import pokemon
from models.pokemon import Pokemon  
from models.trainer import *
from schemes import *
import fastapi.middleware.cors as cors


app = FastAPI()
app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
engine = create_engine('sqlite:///./test.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)

@app.get("/")
def home():
    return JSONResponse(content={"message": "Welcome to pokeServer by Pedro"})

@app.get("/ping")
def ping():
    return JSONResponse(content={"response": "other api pong"})

@app.patch("/updatePlayerLocation/")
async def update_player_location(playerLocationSchema: PlayerLocationSchema):
        db = SessionLocal()
        print(playerLocationSchema.model_dump())
        trainer = db.query(Trainer).filter(Trainer.name == playerLocationSchema.trainer_name).first()
        if not trainer:
            db.close()
            return JSONResponse(content={"error": "Player not found"}, status_code=404)
        trainer.current_location = playerLocationSchema.new_location
        db.commit()
        trainerSchema = TrainerSchema.model_validate(trainer)
        db.close()
        return JSONResponse(trainerSchema.model_dump(), status_code=200)

@app.post("/capturePokemon/")
async def capture_pokemon(capturePokemonSchema: CapturePokemonSchema):
        print("finalmente entrou")
        pokemon = PokemonSchema(**capturePokemonSchema.pokemon.model_dump())
        pokemonDB = Pokemon(**pokemon.model_dump(), trainer_name=capturePokemonSchema.trainer.name)
        db = SessionLocal()
        db.add(pokemonDB)
        db.commit()
        db.refresh(pokemonDB)
        db.close()
        return JSONResponse(content={"pokemon": pokemon.model_dump()}, status_code=200)

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
    

@app.get("/listAllTrainers/")
async def list_all_trainers():
    db = SessionLocal()
    close_db = True
    trainers = db.query(Trainer).all()
    if trainers:
        trainer_schemas = [TrainerSchema.model_validate(trainer) for trainer in trainers]
        if close_db:
            db.close()
        return JSONResponse(content={"trainers": [trainer.model_dump() for trainer in trainer_schemas]}, status_code=200)
    else:
        if close_db:
            db.close()
        return JSONResponse(content={"error": "No trainers found"}, status_code=404)

@app.delete("/deletePokemon")
async def delete_pokemon(deleteInfo: DeletePokemonSchema):
    print("entrou no delete")
    db = SessionLocal()
    close_db = True
    from sqlalchemy import and_
    db_pokemon = db.query(Pokemon).filter(and_(Pokemon.id == deleteInfo.pokemon_id, Pokemon.trainer_name == deleteInfo.trainer_name)).first()
    if db_pokemon:
        db.delete(db_pokemon)
        db.commit()
        pokemonScheme = PokemonSchema.model_validate(db_pokemon)
        if close_db:
            db.close()
        return JSONResponse(content={"message": "Pokemon deleted successfully", "pokemon": pokemonScheme.model_dump()}, status_code=200)
    else:
        if close_db:
            db.close()
        return JSONResponse(content={"error": "Pokemon not found"}, status_code=404)