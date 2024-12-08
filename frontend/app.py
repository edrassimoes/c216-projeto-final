from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from faker import Faker
import requests
import random
import os

app = Flask(__name__)

BASE_URL = os.getenv("BACKEND_URL", "http://backend:8000/api/v1")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cardapio')
def cardapio():
    response = requests.get(f"{BASE_URL}/pratos/")
    pratos = response.json()
    return render_template('cardapio.html', pratos=pratos)

@app.route('/criar_prato', methods=['POST'])
def criar_prato():
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = float(request.form['preco'])
    pessoas = int(request.form['pessoas'])

    prato_data = {
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "pessoas": pessoas
        }

    response = requests.post(f"{BASE_URL}/pratos/", json=prato_data)

    if response.status_code == 200:
        return redirect(url_for('cardapio'))
    else:
        return "Erro ao criar o prato", 500

@app.route('/pedidos')
def pedidos():
    response = requests.get(f"{BASE_URL}/pedidos/")
    pedidos = response.json()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/pedidos', methods=['POST'])
def criar_pedido():
    formas_de_pagamento = ['dinheiro', 'cartao', 'pix']
    fake = Faker('pt_BR')

    cliente = fake.name()
    endereco = fake.address()
    forma_de_pagamento = random.choice(formas_de_pagamento)
    horario = datetime.now().strftime("%d/%m/%Y")

    response_pratos = requests.get(f"{BASE_URL}/pratos/")

    if response_pratos.status_code == 200:
        pratos = response_pratos.json()
        prato_id = random.choice(pratos)['id']
    else:
        return "Erro ao buscar pratos", 500

    # Dados do pedido
    pedido_data = {
        "cliente": cliente,
        "prato_id": prato_id,
        "endereco": endereco,
        "forma_de_pagamento": forma_de_pagamento,
        "horario": horario
    }

    response_pedido = requests.post(f"{BASE_URL}/pedidos/", json=pedido_data)

    if response_pedido.status_code == 200:
        return redirect(url_for('pedidos'))
    else:
        return "Erro ao criar o pedido", 500


if __name__ == '__main__':
    app.run(debug=True)
