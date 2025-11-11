# app/routes/pedido_api.py
from flask import Blueprint, request, jsonify
from app.services.pedido_services import criar_pedido, adicionar_item, calcular_total, finalizar_pedido, remover_item
from app.services.pagamento_services import realizar_pagamento, confirmar_pagamento, cancelar_pagamento
from app.models import Pedido, Produto

pedido_api = Blueprint("pedido_api", __name__)

@pedido_api.route("/pedido", methods=["POST"])
def api_criar_pedido():
    # aceita body vazio ou {"cpf": "..."}
    dados = request.get_json(silent=True) or {}
    cpf = dados.get("cpf")
    resultado = criar_pedido(cpf)
    return jsonify(resultado)


@pedido_api.route("/pedido/<int:pedido_id>/item", methods=["POST"])
def api_adicionar_item(pedido_id):
    dados = request.get_json()
    produto_id = dados.get("produto_id")
    quantidade = dados.get("quantidade", 1)
    return jsonify(adicionar_item(pedido_id, produto_id, quantidade))


@pedido_api.route("/pedido/<int:pedido_id>/item", methods=["DELETE"])
def api_remover_item(pedido_id):
    dados = request.get_json()
    produto_id = dados.get("produto_id")
    quantidade = dados.get("quantidade", 1)
    return jsonify(remover_item(pedido_id, produto_id, quantidade))


@pedido_api.route("/pedido/<int:pedido_id>/total", methods=["GET"])
def api_total_pedido(pedido_id):
    total = calcular_total(pedido_id)
    return jsonify({"total": total})


@pedido_api.route("/pedido/<int:pedido_id>/pagar", methods=["POST"])
def api_realizar_pagamento(pedido_id):
    dados = request.get_json()
    forma = dados.get("forma_pagamento") or dados.get("forma") or dados.get("metodo")
    if not forma:
        return jsonify({"status":"erro","mensagem":"Forma de pagamento não informada."}), 400
    # delega ao serviço de pagamento
    return jsonify(realizar_pagamento(pedido_id, forma))


@pedido_api.route("/pedido/<int:pedido_id>", methods=["GET"])
def api_detalhes_pedido(pedido_id):
    pedido = Pedido.query.get(pedido_id)

    if not pedido:
        return jsonify({"status": "erro", "mensagem": "Pedido não encontrado."}), 404

    itens = []
    for item in pedido.itens:
        itens.append({
            "produto_id": item.produto.id,
            "nome": item.produto.nome,
            "preco": item.produto.preco,
            "quantidade": item.quantidade
        })

    return jsonify({
        "id": pedido.id,
        "status": pedido.status,
        "itens": itens,
        "valor_total": pedido.valor_total
    })


# Lista de produtos para o frontend (GET /api/produtos)
@pedido_api.route("/produtos", methods=["GET"])
def api_listar_produtos():
    produtos = Produto.query.all()
    lista = []
    for p in produtos:
        lista.append({
            "id": p.id,
            "nome": p.nome,
            "descricao": getattr(p, "descricao", ""),
            "preco": p.preco
        })
    return jsonify(lista)
