from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

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

# ----------------------------------------------- PRATOS ---------------------------------------------------------------
@app.post("api/v1/pratos/")
def criar_prato(prato: Prato):
    return {"message": "Prato criado"}

@app.get("api/v1/pratos/")
def listar_pratos():
    return {"message": "Lista de pratos"}

@app.get("api/v1/pratos/{id}")
def listar_prato(id: int):
    return {"message": f"Prato {id} encontrado"}

@app.put("api/v1/pratos/{id}")
def atualizar_prato(id: int, prato: Prato):
    return {"message": f"Prato {id} atualizado"}

@app.delete("/api/v1/pratos/{id}")
def deletar_prato(id: int):
    return {"message": f"Prato {id} deletado"}

# ----------------------------------------------- PEDIDOS --------------------------------------------------------------
@app.post("api/v1/pedidos/")
def criar_pedido(pedido: Pedido):
    return {"message": "Pedido criado"}

@app.get("api/v1/pedidos/")
def listar_pedidos():
    return {"message": "Lista de pedidos"}

@app.get("api/v1/pedidos/{id}")
def listar_pedido(id: int):
    return {"message": f"Pedido {id} encontrado"}

@app.put("api/v1/pedidos/{id}")
def atualizar_pedido(id: int, pedido: Pedido):
    return {"message": f"Pedido {id} atualizado"}

@app.delete("/api/v1/pedidos/{id}")
def deletar_pedido(id: int):
    return {"message": f"Pedido {id} deletado"}