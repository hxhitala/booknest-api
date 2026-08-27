from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    exemplar_id = Column(Integer, ForeignKey("exemplares.id"), nullable=False)
    data_emprestimo = Column(Date, nullable=False)
    data_prevista = Column(Date, nullable=False)
    data_devolucao = Column(Date, nullable=True)  # nulo enquanto não devolvido
    status = Column(String, nullable=False, default="ativo")
    # valores possíveis: "ativo", "devolvido", "atrasado"

    usuario = relationship("Usuario", back_populates="emprestimos")
    exemplar = relationship("Exemplar", back_populates="emprestimos")
    multa = relationship("Multa", back_populates="emprestimo", uselist=False)