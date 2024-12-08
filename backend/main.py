from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import asyncpg
import os

async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/restaurantes")
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
    horario: str

# -----------------------------------------------  CRUD PRATOS ---------------------------------------------------------
@app.post("/api/v1/pratos/")
async def criar_prato(prato: Prato):
    conn = await get_database()
    try:
        query = "INSERT INTO pratos (nome, descricao, preco, pessoas) VALUES ($1, $2, $3, $4)"
        async with conn.transaction():
            result = await conn.execute(query, prato.nome, prato.descricao, prato.preco, prato.pessoas)
            return {"message": "Prato criado"}
    except Exception as e:
        return {"message": "Ocorreu um erro. Tente novamente mais tarde."}
    finally:
        await conn.close()

@app.get("/api/v1/pratos/")
async def listar_pratos():
    conn = await get_database()
    try:
        query = "SELECT * FROM pratos ORDER BY nome"
        rows = await conn.fetch(query)
        pratos = [dict(row) for row in rows]
        return pratos
    except Exception as e:
        return {"message": "Ocorreu um erro. Tente novamente mais tarde."}
    finally:
        await conn.close()

@app.get("/api/v1/pratos/{id}")
async def listar_prato(id: int):
    conn = await get_database()
    try:
        query = "SELECT * FROM pratos WHERE id = $1"
        prato = await conn.fetchrow(query, id)
        return dict(prato)
    except Exception as e:
        return {"message": "Ocorreu um erro. Tente novamente mais tarde."}
    finally:
        await conn.close()


@app.patch("/api/v1/pratos/{id}")
async def atualizar_prato(id: int, dados_atualizar: PratoAtualizar):
    conn = await get_database()
    try:
        query = "SELECT * FROM pratos WHERE id = $1"
        prato = await conn.fetchrow(query, id)
        update = """
            UPDATE pratos SET 
            nome = COALESCE($2, nome),
            descricao = COALESCE($3, descricao),
            preco = COALESCE($4, preco),
            pessoas = COALESCE($5, pessoas)
            WHERE id = $1
        """
        await conn.execute(update, id, dados_atualizar.nome, dados_atualizar.descricao,dados_atualizar.preco, dados_atualizar.pessoas)
        return {"message": "Prato atualizado"}
    except Exception as e:
        return {"message": f"Ocorreu um erro. Tente novamente mais tarde. Erro: {str(e)}"}
    finally:
        await conn.close()

@app.delete("/api/v1/pratos/{id}")
async def deletar_prato(id: int):
    conn = await get_database()
    try:
        delete_pedidos_query = "DELETE FROM pedidos WHERE prato_id = $1 "
        await conn.execute(delete_pedidos_query, id)
        delete_prato_query = "DELETE FROM pratos WHERE id = $1"
        await conn.execute(delete_prato_query, id)
        return {"message": "Prato e seus pedidos vinculados foram deletados com sucesso"}
    except Exception as e:
        return {"message": f"Ocorreu um erro: {str(e)}"}
    finally:
        await conn.close()

# ----------------------------------------------- CRUD PEDIDOS ---------------------------------------------------------

# Não será utilizada.
@app.post("/api/v1/pedidos/")
async def criar_pedido(id: int):
    return {"message": f"Pedido {id} criado"}

@app.get("/api/v1/pedidos/")
async def get_pedidos():
    conn = await get_database()
    try:
        query = "SELECT * FROM pedidos"
        rows = await conn.fetch(query)
        pedidos = [dict(row) for row in rows]
        return pedidos
    except Exception as e:
        return {"message": "Ocorreu um erro. Tente novamente mais tarde."}
    finally:
        await conn.close()

# Não será utilizada.
@app.get("/api/v1/pedidos/{id}")
async def listar_pedido(id: int):
    return {"message": f"Pedido {id} encontrado"}

# Não será utilizada.
@app.patch("/api/v1/pedidos/{id}")
async def atualizar_pedido(id: int, pedido: Pedido):
    return {"message": f"Pedido {id} atualizado"}

# Não será utilizada.
@app.delete("/api/v1/pedidos/{id}")
async def deletar_pedido(id: int):
    return {"message": f"Pedido {id} deletado"}

# ----------------------------------------------- RESET DO BANCO -------------------------------------------------------
@app.delete("/api/v1/pratos/")
async def reset_data():
    init_sql = os.getenv("INIT_SQL", "postgresql/init.sql")
    conn = await get_database()
    try:
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        await conn.execute(sql_commands)
        return {"message": "Banco de dados limpo com sucesso!"}
    finally:
        await conn.close()

reset_data()
