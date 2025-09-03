from sqlalchemy import PrimaryKeyConstraint, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class Pokemon(Base):
    __tablename__ = 'pokemons'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)
    trainer_name = Column(String, ForeignKey('trainer.name'), primary_key=True)
    trainer = relationship("Trainer", back_populates="pokemons")

    #__table_args__ = (PrimaryKeyConstraint('id', 'trainer_name'))

    def __init__(self, id: int, name: str, weight: int, trainer_name: str):
        self.id = id
        self.name = name
        self.weight = weight
        self.trainer_name = trainer_name
