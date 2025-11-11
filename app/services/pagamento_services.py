# app/services/pagamento_services.py
from app.models import db, Pedido, Pagamento
from app.services.pedido_services import calcular_total

def realizar_pagamento(pedido_id, forma_pagamento):
    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        return {"status": "erro", "mensagem": "Pedido não encontrado."}

    total = calcular_total(pedido_id)

    pagamento = Pagamento(
        pedido_id=pedido_id,
        valor_total=total,
        forma_pagamento=forma_pagamento,
        status_pagamento="em_andamento"
    )

    db.session.add(pagamento)
    db.session.commit()

    return {"status": "ok", "mensagem": "Pagamento iniciado.", "pagamento_id": pagamento.id, "total": total}


def confirmar_pagamento(pagamento_id):
    pagamento = Pagamento.query.get(pagamento_id)
    if not pagamento:
        return {"status": "erro", "mensagem": "Pagamento não encontrado."}

    pagamento.status_pagamento = "aprovado"
    pagamento.pedido.status = "concluido"

    db.session.commit()
    return {"status": "ok", "mensagem": "Pagamento aprovado e pedido concluído."}


def cancelar_pagamento(pagamento_id):
    pagamento = Pagamento.query.get(pagamento_id)
    if not pagamento:
        return {"status": "erro", "mensagem": "Pagamento não encontrado."}

    pagamento.status_pagamento = "cancelado"
    pagamento.pedido.status = "cancelado"

    db.session.commit()
    return {"status": "ok", "mensagem": "Pagamento cancelado e pedido cancelado."}
