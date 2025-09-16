from pydantic import BaseModel
from typing import Optional, List
from .pokemonSchema import PokemonSchema

class TrainerSchema(BaseModel):
    """ Define como um novo treinador a ser inserido deve ser representado
    """
    name: str = "John Doe"
    number_of_encounters: int = 0
    current_location: str = "Unknown"
    id: Optional[int] = None

    class Config:
        from_attributes = True

class UpdatePlayerLocationSchema(BaseModel):
    trainer_id: int
    new_location: str

    class Config:
        from_attributes = True

class CapturePokemonTrainerSchema(BaseModel):
    id: int

    class Config:
        from_attributes = True


class CapturePokemonSchema(BaseModel):
    trainer: CapturePokemonTrainerSchema
    pokemon: PokemonSchema

    class Config:
        from_attributes = True
        
