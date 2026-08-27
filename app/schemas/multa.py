from pydantic import BaseModel
from decimal import Decimal
from datetime import date


class MultaResponse(BaseModel):
    id: int
    emprestimo_id: int
    valor: Decimal
    paga: bool
    data_geracao: date

    class Config:
        from_attributes = True
    # não existe MultaCreate — multa nunca é criada
    # diretamente pelo cliente via API, ela é gerada automaticamente
    # pelo service quando um empréstimo é devolvido com atraso