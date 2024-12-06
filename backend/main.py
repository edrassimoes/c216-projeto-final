from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
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

class PratoAtualizar(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    pessoas: Optional[int] = None

class Pedido(BaseModel):
    cliente: str
    prato_id: int
    endereco: str
    forma_pagamento: str
    horario: datetime = datetime.now()

# -----------------------------------------------  CRUD PRATOS ---------------------------------------------------------
@app.post("api/v1/pratos/")
async def criar_prato(prato: Prato):
    conn = await get_database()
    try:
        query = "INSERT INTO pratos (nome, descricao, preco, pessoas) VALUES ($1, $2, $3, $4)"
        async with conn.transaction():
            result = await conn.execute(query, prato.nome, prato.descricao, prato.preco, prato.pessoas)
            return {"message": "Prato criado"}
    except Exception as e:
        return {"message": str(e)}
    finally:
        await conn.close()

@app.get("api/v1/pratos/")
async def listar_pratos():
    conn = await get_database()
    try:
        query = "SELECT * FROM pratos ORDER BY nome"
        rows = await conn.fetch(query)
        pratos = [dict(row) for row in rows]
        return pratos
    except Exception as e:
        return {"message": str(e)}
    finally:
        await conn.close()

@app.get("api/v1/pratos/{id}")
async def listar_prato(id: int):
    conn = await get_database()
    try:
        query = "SELECT * FROM pratos WHERE id = $1"
        prato = await conn.fetchrow(query, id)
        return dict(prato)
    except Exception as e:
        return {"message": str(e)}
    finally:
        await conn.close()

@app.patch("api/v1/pratos/{id}")
async def atualizar_prato(id: int, prato: PratoAtualizar):
    conn = await get_database()
    try:
        query = "SELECT * FROM pratos WHERE id = $1"
        prato = await conn.fetchrow(query, id)
        update = """
            UPDATE pratos
            SET nome = COALESCE($1, nome),
            descricao = COALESCE($2, descricao),
            preco = COALESCE($3, preco),
            pessoas = COALESCE($4, pessoas),
            WHERE id = COALESCE($5, id)
        """
        await conn.execute(update, prato.nome, prato.descricao, prato.preco, prato.pessoas, prato.id)
        return {"message": "Prato atualizado"}
    except Exception as e:
        return {"message": str(e)}
    finally:
        await conn.close()

@app.delete("/api/v1/pratos/{id}")
async def deletar_prato(id: int):
    conn = await get_database()
    try:
        query = "DELETE FROM pratos WHERE id = $1"
        prato = await conn.fetchrow(query, id)
        return {"message": "Prato deletado"}
    except Exception as e:
        return {"message": str(e)}
    finally:
        await conn.close()

# ----------------------------------------------- CRUD PEDIDOS ---------------------------------------------------------
@app.post("api/v1/pedidos/")
async def criar_pedido(pedido: Pedido):
    conn = await get_database()
    try:
        query = 'SELECT * FROM pratos WHERE id = $1'
        prato = await conn.fetchrow(query, pedido.id)
        put = 'INSERT INTO pedidos (cliente, prato_id, endereco, forma_pagamento, horario) VALUES ($1, $2, $3, $4, $5)'
        await conn.execute(put, pedido.cliente, pedido.id, pedido.endereco, pedido.forma_pagamento, pedido.horario)
        return {"message": "Pedido criado"}
    except Exception as e:
        return {"message": str(e)}
    finally:
        await conn.close()

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