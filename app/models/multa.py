from sqlalchemy import Column, Integer, Numeric, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Multa(Base):
    __tablename__ = "multas"

    id = Column(Integer, primary_key=True, index=True)
    emprestimo_id = Column(Integer, ForeignKey("emprestimos.id"), nullable=False, unique=True)
    valor = Column(Numeric(10, 2), nullable=False)
    paga = Column(Boolean, nullable=False, default=False)
    data_geracao = Column(Date, nullable=False)

    emprestimo = relationship("Emprestimo", back_populates="multa")