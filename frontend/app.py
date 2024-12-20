from flask import Flask, render_template, request, redirect, url_for
import requests
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

@app.route('/criar_prato', methods=['GET','POST'])
def criar_prato():
    if request.method == 'POST':
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

    else:
        return render_template('criar_prato.html')

@app.route('/pedidos')
def pedidos():
    response = requests.get(f"{BASE_URL}/pedidos/")
    lista = response.json()
    return render_template('pedidos.html', pedidos=lista)

@app.route('/reset_database', methods=['GET'])
def reset_database():
    response = requests.delete(f"{BASE_URL}/pratos/")

    if response.status_code == 200:
        return render_template('index.html')
    else:
        return "Erro ao resetar o database", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

