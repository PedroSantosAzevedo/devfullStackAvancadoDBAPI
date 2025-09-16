from sqlalchemy import PrimaryKeyConstraint, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class Pokemon(Base):
    __tablename__ = 'pokemons'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)
    trainer_id = Column(Integer, ForeignKey('trainer.id'), primary_key=True)
    trainer = relationship("Trainer", back_populates="pokemons")

    def __init__(self, id: int, name: str, weight: int, trainer_id: int ):
        self.id = id
        self.name = name
        self.weight = weight
        self.trainer_id = trainer_id
