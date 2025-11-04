from flask import render_template, request, jsonify
from app import app
from app.models import Pagamento, Reserva_Mesa, Cliente
import datetime
import pickle as pkl
import os

RESERVAS_FILE = 'app/models/mesas.pkl'

# Função para carregar reservas do pickle
def carregar_reservas():
    if os.path.exists(RESERVAS_FILE):
        with open(RESERVAS_FILE, 'rb') as f:
            return pkl.load(f)
    return [[] for _ in range(10)]  # 10 mesas

# Função para salvar reservas no pickle
def salvar_reservas(mesas):
    with open(RESERVAS_FILE, 'wb') as f:
        pkl.dump(mesas, f)

# Home Page
@app.route("/")
def home():
    return render_template("index.html", title="La Forchetta 🍝")


# Página de reservas
@app.route("/reserva_mesa")
def reservas_page():
    return render_template("reserva_mesa.html", title="Reservas - La Forchetta")

# API para listar reservas
@app.route("/api/reservas", methods=["GET"])
def api_get_reservas():
    mesas = carregar_reservas()
    lista = []
    for numero_mesa, reservas_mesa in enumerate(mesas, start=1):
        for i in range(0, len(reservas_mesa), 2):
            lista.append({
                "numero_mesa": numero_mesa,
                "horario_de_entrada": reservas_mesa[i].strftime("%H:%M"),
                "horario_de_saida": reservas_mesa[i+1].strftime("%H:%M"),
                "data": reservas_mesa[i].strftime("%Y-%m-%d"),
                "cliente": "Reservado"
            })
    return jsonify({"status": "ok", "reservas": lista})

# API para criar reserva
@app.route("/api/reservas", methods=["POST"])
def api_post_reserva():
    try:
        dados = request.get_json()
        nome = dados['nome']
        mesa = int(dados['mesa'])
        data_str = dados['data']
        entrada_str = dados['entrada']
        saida_str = dados['saida']

        # Converte data e horários para datetime
        horario_entrada = datetime.datetime.strptime(f"{data_str} {entrada_str}", "%Y-%m-%d %H:%M")
        horario_saida = datetime.datetime.strptime(f"{data_str} {saida_str}", "%Y-%m-%d %H:%M")

        if horario_entrada >= horario_saida:
            return jsonify({"status": "erro", "mensagem": "Horário de saída deve ser depois da entrada."})

        # Checa horário permitido (11h às 23h)
        if not (11 <= horario_entrada.hour < 23) or not (11 < horario_saida.hour <= 23):
            return jsonify({"status": "erro", "mensagem": "Horário permitido das 11h às 23h."})

        cliente = Cliente(None, nome)
        reserva_obj = Reserva_Mesa(cliente, horario_entrada, horario_saida, mesa)

        resultado = reserva_obj.reservar_mesa()
        if resultado == 0:
            return jsonify({"status": "erro", "mensagem": f"Mesa {mesa} já reservada nesse horário."})

        return jsonify({"status": "ok", "mensagem": f"Reserva feita com sucesso para {nome} na mesa {mesa}!"})

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": f"Erro ao criar reserva: {e}"})
    


# Rota para a conexão do front com back com o pagamento
@app.route("/api/pagamento", methods=["POST"])
def processar_pagamento():
    try:
        dados = request.get_json()
        valor_total = float(dados.get("valor_total", 0))
        metodo = dados.get("metodo")

        if valor_total <= 0:
            return jsonify({"status": "erro", "mensagem": "Valor inválido para pagamento."})

        if metodo not in ["Pix", "Cartão de crédito/débito", "Dinheiro"]:
            return jsonify({"status": "erro", "mensagem": "Método de pagamento inválido."})

        pagamento = Pagamento(valor_total, metodo)
        resultado = pagamento.processar_pagamento()

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)})