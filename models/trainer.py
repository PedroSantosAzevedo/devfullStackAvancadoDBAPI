from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union
from .base import Base

class Trainer(Base):

    __tablename__ = 'trainer'

    name = Column(String(50),primary_key=True, nullable=False)
    number_of_encounters = Column(Integer, default=0)
    current_location = Column(String(100), nullable=True)

    def __init__(self, name: str,  number_of_encounters: int, current_location: str):
        self.name = name
        self.number_of_encounters = number_of_encounters
        self.current_location = current_location

    def to_dict(self):
        return {
            "name": self.name,
            "number_of_encounters": self.number_of_encounters,
            "current_location": self.current_location
        }