from pydantic import BaseModel

class PlayerLocationSchema(BaseModel):
    """ Define como um novo treinador a ser inserido deve ser representado
    """
    trainer_id: int
    new_location: str

    class Config:
        from_attributes = True
