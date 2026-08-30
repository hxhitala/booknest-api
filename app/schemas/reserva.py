from pydantic import BaseModel
from datetime import date


class ReservaBase(BaseModel):
    usuario_id: int
    livro_id: int


class ReservaCreate(BaseModel):
    livro_id: int
    # usuario_id não é mais enviado pelo cliente — vem do token


class ReservaResponse(ReservaBase):
    id: int
    data_reserva: date
    status: str

    class Config:
        from_attributes = True