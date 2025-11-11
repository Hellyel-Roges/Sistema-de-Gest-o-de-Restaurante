# app/services/pedido_services.py
from app.models import db, Cliente, Produto, Pedido, PedidoProduto
from datetime import datetime

def criar_pedido(cpf_cliente=None):
    """
    Cria um pedido aberto. cpf_cliente é opcional (pode ser None).
    Retorna dict com status e id do pedido.
    """
    cliente = None
    if cpf_cliente:
        cliente = Cliente.query.filter_by(cpf=cpf_cliente).first()

    pedido = Pedido(cliente_id = cliente.id if cliente else None, status="aberto", data_pedido=datetime.now())
    db.session.add(pedido)
    db.session.commit()

    return {"status": "ok", "id": pedido.id, "mensagem": "Pedido criado com sucesso."}


def adicionar_item(pedido_id, produto_id, quantidade=1):
    pedido = Pedido.query.get(pedido_id)
    produto = Produto.query.get(produto_id)

    if not pedido:
        return {"status": "erro", "mensagem": "Pedido não encontrado."}
    if not produto:
        return {"status": "erro", "mensagem": "Produto não encontrado."}

    item = PedidoProduto.query.filter_by(pedido_id=pedido_id, produto_id=produto_id).first()

    if item:
        item.quantidade += int(quantidade)
    else:
        item = PedidoProduto(pedido_id=pedido_id, produto_id=produto_id, quantidade=int(quantidade))
        db.session.add(item)

    db.session.commit()
    return {"status": "ok", "mensagem": f"{quantidade}x {produto.nome} adicionado(s) ao pedido."}


def remover_item(pedido_id, produto_id, quantidade=1):
    item = PedidoProduto.query.filter_by(pedido_id=pedido_id, produto_id=produto_id).first()

    if not item:
        return {"status": "erro", "mensagem": "Item não está no pedido."}

    if item.quantidade > quantidade:
        item.quantidade -= quantidade
    else:
        db.session.delete(item)

    db.session.commit()
    return {"status": "ok", "mensagem": "Item atualizado/removido com sucesso."}


def calcular_total(pedido_id):
    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        return None

    total = 0.0
    for item in pedido.itens:
        total += item.quantidade * item.produto.preco

    return float(total)


def finalizar_pedido(pedido_id):
    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        return {"status": "erro", "mensagem": "Pedido não encontrado."}

    total = calcular_total(pedido_id)
    pedido.valor_total = total
    pedido.status = "finalizado"

    db.session.commit()
    return {"status": "ok", "mensagem": "Pedido finalizado com sucesso.", "total": total}
