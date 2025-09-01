from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from models import Base

class Pokemon(Base):
    __tablename__ = 'pokemons'
    
    # Using an auto-incrementing ID as primary key for Pokémon
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)
    trainer_name = Column(String, ForeignKey('trainer.name'))


    def __init__(self, id: int, name: str, weight: int, trainer_name: str):
        self.id = id
        self.name = name
        self.weight = weight
        self.trainer_name = trainer_name