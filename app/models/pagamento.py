from app.models.database import db
from datetime import datetime

class Pagamento(db.Model):
    __tablename__ = "pagamentos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor_total = db.Column(db.Float, nullable=False)

    forma_pagamento = db.Column(db.String(20), nullable=False)
    # cartao_credito | cartao_debito | pix | dinheiro

    status_pagamento = db.Column(db.String(20), default="em_andamento")
    # em_andamento | aprovado | cancelado

    data_pagamento = db.Column(db.DateTime, default=datetime.now)

    # FK -> Pedido
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    pedido = db.relationship("Pedido", back_populates="pagamento")

    def __repr__(self):
        return f"<Pagamento Pedido={self.pedido_id} Status={self.status_pagamento}>"
