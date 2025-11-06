from flask import Blueprint, request, jsonify
from app.services.reserva_services import criar_reserva
from app.models import ReservaMesa

reservas_api = Blueprint("reservas_api", __name__)

@reservas_api.route("/reservas", methods=["POST"])
def api_post_reserva():
    dados = request.get_json()
    resultado = criar_reserva(
        nome_cliente=dados['nome'],
        numero_mesa=int(dados['mesa']),
        data_str=dados['data'],
        entrada_str=dados['entrada'],
        saida_str=dados['saida']
    )
    return jsonify(resultado)

@reservas_api.route("/reservas", methods=["GET"])
def api_get_reservas():
    reservas = ReservaMesa.query.all()
    lista = []
    for r in reservas:
        lista.append({
            "numero_mesa": r.numero_mesa,
            "data": r.horario_de_entrada.strftime("%Y-%m-%d"),
            "horario_de_entrada": r.horario_de_entrada.strftime("%H:%M"),
            "horario_de_saida": r.horario_de_saida.strftime("%H:%M"),
            "cliente": r.cliente.nome
        })
    return jsonify({"status": "ok", "reservas": lista})
