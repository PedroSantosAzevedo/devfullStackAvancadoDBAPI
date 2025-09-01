from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TrainerSchema(BaseModel):
    """ Define como um novo treinador a ser inserido deve ser representado
    """
    name: str = "John Doe"
    number_of_encounters: int = 0
    current_location: str = "Unknown"

    class Config:
        from_attributes = True
