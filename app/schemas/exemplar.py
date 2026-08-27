from pydantic import BaseModel


class ExemplarBase(BaseModel):
    livro_id: int
    status: str = "disponivel"


class ExemplarCreate(ExemplarBase):
    pass


class ExemplarResponse(ExemplarBase):
    id: int

    class Config:
        from_attributes = True