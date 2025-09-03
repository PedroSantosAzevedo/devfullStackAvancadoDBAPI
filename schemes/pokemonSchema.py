from pydantic import BaseModel
from .trainerSchema import TrainerSchema

class PokemonSchema(BaseModel):
    """ Define como um novo pokemon a ser inserido deve ser representado
    """
    id: int = 1
    name: str = "bulbassauro"
    weight: int = 30

    class Config:
        from_attributes = True
