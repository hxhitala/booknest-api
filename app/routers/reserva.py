from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.reserva import ReservaCreate, ReservaResponse
from app.models.reserva import Reserva
from app.services import reserva_service

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post("/", response_model=ReservaResponse, status_code=201)
def criar_reserva(dados: ReservaCreate, db: Session = Depends(get_db)):
    return reserva_service.criar_reserva(
        db=db, usuario_id=dados.usuario_id, livro_id=dados.livro_id
    )


@router.post("/{reserva_id}/cancelar", response_model=ReservaResponse)
def cancelar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    return reserva_service.cancelar_reserva(db=db, reserva_id=reserva_id)


@router.get("/", response_model=List[ReservaResponse])
def listar_reservas(db: Session = Depends(get_db)):
    return db.query(Reserva).all()


@router.get("/usuario/{usuario_id}", response_model=List[ReservaResponse])
def listar_reservas_do_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(Reserva).filter(Reserva.usuario_id == usuario_id).all()