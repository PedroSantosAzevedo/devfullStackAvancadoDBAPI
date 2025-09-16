from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy import PrimaryKeyConstraint, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from typing import Union
from .base import Base

class Trainer(Base):

    __tablename__ = 'trainer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    number_of_encounters = Column(Integer, default=0)
    current_location = Column(String(100), nullable=True)
    
    pokemons = relationship("Pokemon", back_populates="trainer", cascade="all, delete-orphan")

    def __init__(self, name: str,  number_of_encounters: int, current_location: str, id: int):
        self.name = name
        self.number_of_encounters = number_of_encounters
        self.current_location = current_location
        self.pokemons = []
        self.id = id

    class Config:
        from_attributes = True