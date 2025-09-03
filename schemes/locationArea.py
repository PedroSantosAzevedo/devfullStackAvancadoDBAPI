from pydantic import BaseModel
from typing import Optional,List

class NamedAPIResource(BaseModel):
    name: str
    url: str

class EncounterMethodRateVersionDetail(BaseModel):
    rate: int
    version: NamedAPIResource

class EncounterMethodRate(BaseModel):
    encounter_method: NamedAPIResource
    version_details: List[EncounterMethodRateVersionDetail]

class Name(BaseModel):
    name: str
    language: NamedAPIResource

class EncounterDetail(BaseModel):
    min_level: int
    max_level: int
    condition_values: List
    chance: int
    method: NamedAPIResource

class PokemonEncounter(BaseModel):
    pokemon: NamedAPIResource
    class Config:
        extra = "ignore"

class LocationArea(BaseModel):
    id: int
    name: str
    location: NamedAPIResource
    pokemon_encounters: List[PokemonEncounter]
    class Config:
        extra = "ignore"