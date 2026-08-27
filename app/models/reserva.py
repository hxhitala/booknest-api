from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    livro_id = Column(Integer, ForeignKey("livros.id"), nullable=False)
    data_reserva = Column(Date, nullable=False)
    status = Column(String, nullable=False, default="pendente")
    # valores possíveis: "pendente", "atendida", "cancelada"

    usuario = relationship("Usuario", back_populates="reservas")
    livro = relationship("Livro", back_populates="reservas")