from pydantic import BaseModel
from typing import Optional,List


class Region(BaseModel):
    name: str
    url: str

class Area(BaseModel):
    name: str
    url: str

class Location(BaseModel):
    id: int
    name: str
    region: Region
    areas: List[Area]
    class Config:
        extra = "ignore"