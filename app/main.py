from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import autor, categoria

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BookNest API")

app.include_router(autor.router)
app.include_router(categoria.router)


@app.get("/")
def raiz():
    return {"mensagem": "BookNest API rodando"}