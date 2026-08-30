from pydantic import BaseModel
from datetime import date
from typing import Optional


class EmprestimoBase(BaseModel):
    usuario_id: int
    exemplar_id: int


class EmprestimoCreate(BaseModel):
    exemplar_id: int
    # usuario_id não é mais enviado pelo cliente — vem do token


class EmprestimoResponse(EmprestimoBase):
    id: int
    data_emprestimo: date
    data_prevista: date
    data_devolucao: Optional[date] = None
    status: str

    class Config:
        from_attributes = True


class DevolucaoRequest(BaseModel):
    exemplar_id: int