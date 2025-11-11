from flask import Blueprint, jsonify
from app.models.produto import Produto

produto_api = Blueprint("produto_api", __name__)

@produto_api.route("/produtos", methods=["GET"])
def api_listar_produtos():
    produtos = Produto.query.all()
    return jsonify([
        {
            "id": p.id,
            "nome": p.nome,
            "descricao": p.descricao,
            "preco": p.preco
        }
        for p in produtos
    ])
