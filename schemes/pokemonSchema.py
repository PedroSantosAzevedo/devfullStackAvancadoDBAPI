from pydantic import BaseModel

class PokemonSchema(BaseModel):
    """ Define como um novo pokemon a ser inserido deve ser representado
    """
    id: int = 1
    name: str = "bulbassauro"
    weight: int = 30

    class Config:
        from_attributes = True

class DeletePokemonSchema(BaseModel):
    """ Define como um pokemon a ser deletado deve ser representado
    """
    trainer_name: str = "John Doe"
    pokemon_id: int = 1

    class Config:
        from_attributes = True

class EncounterPokemonSchema(BaseModel):
    """ Define como um pokemon a ser deletado deve ser representado
    """
    trainer_name: str = "John Doe"
    pokemon_id: int = 1

    class Config:
        from_attributes = True