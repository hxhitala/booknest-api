from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    senha: str  # senha em texto puro, só nesse momento — vai ser hasheada no service


class UsuarioResponse(UsuarioBase):
    id: int
    tipo: str
    criado_em: datetime

    class Config:
        from_attributes = True  # permite converter direto de um objeto SQLAlchemy