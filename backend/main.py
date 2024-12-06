from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import asyncpg
import os

async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/jogos")
    return await asyncpg.connect(DATABASE_URL)

app = FastAPI()

class Prato(BaseModel):
    nome: str
    descricao: str
    preco: float
    pessoas: int

class Pedido(BaseModel):
    cliente: str
    prato_id: int
    endereco: str
    forma_pagamento: str
    horario: datetime = datetime.now()

# -----------------------------------------------  CRUD PRATOS ---------------------------------------------------------
@app.post("api/v1/pratos/")
async def criar_prato(prato: Prato):
    return {"message": "Prato criado"}

@app.get("api/v1/pratos/")
async def listar_pratos():
    return {"message": "Lista de pratos"}

@app.get("api/v1/pratos/{id}")
async def listar_prato(id: int):
    return {"message": f"Prato {id} encontrado"}

@app.patch("api/v1/pratos/{id}")
async def atualizar_prato(id: int, prato: Prato):
    return {"message": f"Prato {id} atualizado"}

@app.delete("/api/v1/pratos/{id}")
async def deletar_prato(id: int):
    return {"message": f"Prato {id} deletado"}

# ----------------------------------------------- CRUD PEDIDOS ---------------------------------------------------------
@app.post("api/v1/pedidos/")
async def criar_pedido(pedido: Pedido):
    return {"message": "Pedido criado"}

@app.get("api/v1/pedidos/")
async def listar_pedidos():
    return {"message": "Lista de pedidos"}

@app.get("api/v1/pedidos/{id}")
async def listar_pedido(id: int):
    return {"message": f"Pedido {id} encontrado"}

@app.patch("api/v1/pedidos/{id}")
async def atualizar_pedido(id: int, pedido: Pedido):
    return {"message": f"Pedido {id} atualizado"}

@app.delete("/api/v1/pedidos/{id}")
async def deletar_pedido(id: int):
    return {"message": f"Pedido {id} deletado"}
# ----------------------------------------------- RESET DO BANCO -------------------------------------------------------
@app.delete("/api/v1/pratos/")
async def reset_data():
    return {"message": "Banco de dados resetado"}