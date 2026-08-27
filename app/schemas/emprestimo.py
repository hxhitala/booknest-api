from pydantic import BaseModel
from datetime import date
from typing import Optional


class EmprestimoBase(BaseModel):
    usuario_id: int
    exemplar_id: int


class EmprestimoCreate(EmprestimoBase):
    pass
    # o cliente NÃO envia data_emprestimo nem data_prevista.
    # Isso vai ser calculado no service (hoje + prazo de 14 dias),
    # nunca confiamos em datas vindas do cliente pra regra de negócio.


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
    # schema minúsculo e específico só pro endpoint de devolução —
    # não reaproveita EmprestimoCreate porque a intenção é outra