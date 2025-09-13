from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .pokemonSchema import PokemonSchema

class TrainerSchema(BaseModel):
    """ Define como um novo treinador a ser inserido deve ser representado
    """
    name: str = "John Doe"
    number_of_encounters: int = 0
    current_location: str = "Unknown"
    # pokemons: List[PokemonSchema] = []

    class Config:
        from_attributes = True

class UpdatePlayerLocationSchema(BaseModel):
    trainer_name: str
    new_location: str

    class Config:
        from_attributes = True

class CapturePokemonTrainerSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CapturePokemonSchema(BaseModel):
    trainer: CapturePokemonTrainerSchema
    pokemon: PokemonSchema

    class Config:
        from_attributes = True
        
