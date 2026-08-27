from pydantic import BaseModel
from datetime import date


class ReservaBase(BaseModel):
    usuario_id: int
    livro_id: int


class ReservaCreate(ReservaBase):
    pass


class ReservaResponse(ReservaBase):
    id: int
    data_reserva: date
    status: str

    class Config:
        from_attributes = True