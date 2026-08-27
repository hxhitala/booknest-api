from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.emprestimo import Emprestimo
from app.models.exemplar import Exemplar
from app.models.multa import Multa

LIMITE_EMPRESTIMOS_SIMULTANEOS = 3
PRAZO_EMPRESTIMO_DIAS = 14
VALOR_MULTA_POR_DIA = Decimal("1.00")


def criar_emprestimo(db: Session, usuario_id: int, exemplar_id: int) -> Emprestimo:
    # Regra 1: usuário não pode ter multa pendente
    multa_pendente = (
        db.query(Multa)
        .join(Emprestimo)
        .filter(Emprestimo.usuario_id == usuario_id, Multa.paga == False)
        .first()
    )
    if multa_pendente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário possui multa pendente e não pode realizar novos empréstimos.",
        )

    # Regra 2: limite de empréstimos simultâneos
    emprestimos_ativos = (
        db.query(Emprestimo)
        .filter(Emprestimo.usuario_id == usuario_id, Emprestimo.status == "ativo")
        .count()
    )
    if emprestimos_ativos >= LIMITE_EMPRESTIMOS_SIMULTANEOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Usuário já atingiu o limite de {LIMITE_EMPRESTIMOS_SIMULTANEOS} empréstimos simultâneos.",
        )

    # Regra 3: exemplar precisa estar disponível
    exemplar = db.query(Exemplar).filter(Exemplar.id == exemplar_id).first()
    if not exemplar:
        raise HTTPException(status_code=404, detail="Exemplar não encontrado.")
    if exemplar.status != "disponivel":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exemplar não está disponível para empréstimo.",
        )

    # Tudo certo: cria o empréstimo e marca o exemplar como emprestado
    hoje = date.today()
    novo_emprestimo = Emprestimo(
        usuario_id=usuario_id,
        exemplar_id=exemplar_id,
        data_emprestimo=hoje,
        data_prevista=hoje + timedelta(days=PRAZO_EMPRESTIMO_DIAS),
        status="ativo",
    )
    exemplar.status = "emprestado"

    db.add(novo_emprestimo)
    db.commit()
    db.refresh(novo_emprestimo)
    return novo_emprestimo


def devolver_emprestimo(db: Session, exemplar_id: int) -> Emprestimo:
    emprestimo = (
        db.query(Emprestimo)
        .filter(Emprestimo.exemplar_id == exemplar_id, Emprestimo.status == "ativo")
        .first()
    )
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Não há empréstimo ativo para esse exemplar.")

    hoje = date.today()
    emprestimo.data_devolucao = hoje
    emprestimo.status = "devolvido"

    # Libera o exemplar
    emprestimo.exemplar.status = "disponivel"

    # Calcula multa se houve atraso
    dias_atraso = (hoje - emprestimo.data_prevista).days
    if dias_atraso > 0:
        multa = Multa(
            emprestimo_id=emprestimo.id,
            valor=Decimal(dias_atraso) * VALOR_MULTA_POR_DIA,
            paga=False,
            data_geracao=hoje,
        )
        db.add(multa)

    db.commit()
    db.refresh(emprestimo)
    return emprestimo