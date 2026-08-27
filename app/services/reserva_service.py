from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.reserva import Reserva
from app.models.exemplar import Exemplar
from app.models.livro import Livro


def criar_reserva(db: Session, usuario_id: int, livro_id: int) -> Reserva:
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    # Regra: só pode reservar se NÃO houver exemplar disponível
    exemplar_disponivel = (
        db.query(Exemplar)
        .filter(Exemplar.livro_id == livro_id, Exemplar.status == "disponivel")
        .first()
    )
    if exemplar_disponivel:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Há exemplares disponíveis, faça o empréstimo diretamente em vez de reservar.",
        )

    # Regra: usuário não pode ter reserva pendente duplicada do mesmo livro
    reserva_existente = (
        db.query(Reserva)
        .filter(
            Reserva.usuario_id == usuario_id,
            Reserva.livro_id == livro_id,
            Reserva.status == "pendente",
        )
        .first()
    )
    if reserva_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já possui uma reserva pendente para este livro.",
        )

    nova_reserva = Reserva(
        usuario_id=usuario_id,
        livro_id=livro_id,
        data_reserva=date.today(),
        status="pendente",
    )
    db.add(nova_reserva)
    db.commit()
    db.refresh(nova_reserva)
    return nova_reserva


def cancelar_reserva(db: Session, reserva_id: int) -> Reserva:
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")
    if reserva.status != "pendente":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Só é possível cancelar reservas pendentes.",
        )

    reserva.status = "cancelada"
    db.commit()
    db.refresh(reserva)
    return reserva