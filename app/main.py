from fastapi import FastAPI
from app.database import Base, engine
from app import models  # importa o __init__.py, que traz todos os models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BookNest API")


@app.get("/")
def raiz():
    return {"mensagem": "BookNest API rodando"}