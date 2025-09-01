from pydantic import BaseModel

class PokemonSchema(BaseModel):
    """ Define como um novo pokemon a ser inserido deve ser representado
    """
    id: int = 1
    name: str = "bulbassauro"
    weight: int = 30


def show_pokemon(pokemon: PokemonSchema):
    """ Exibe as informações de um Pokémon
    """
    return {
        "id": pokemon.id,
        "name": pokemon.name,
        "weight": pokemon.weight
    }