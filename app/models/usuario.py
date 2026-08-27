from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    tipo = Column(String, nullable=False, default="leitor")  # "leitor" ou "admin"
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos (facilita navegar: usuario.emprestimos, usuario.reservas)
    emprestimos = relationship("Emprestimo", back_populates="usuario")
    reservas = relationship("Reserva", back_populates="usuario")