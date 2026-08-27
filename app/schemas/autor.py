from pydantic import BaseModel


class AutorBase(BaseModel):
    nome: str


class AutorCreate(AutorBase):
    pass


class AutorResponse(AutorBase):
    id: int

    class Config:
        from_attributes = True