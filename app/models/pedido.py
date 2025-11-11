# app/models/pedido.py
from app.models.database import db
from datetime import datetime

class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_pedido = db.Column(db.DateTime, default=datetime.now)

    # Status do pedido
    status = db.Column(db.String(20), default="em_andamento")  

    # Relação com Cliente -> agora aceitamos pedido sem cliente (nullable=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=True)
    cliente = db.relationship("Cliente", back_populates="pedidos")

    # Relação N:N com Produto
    itens = db.relationship("PedidoProduto", back_populates="pedido")

        # **Novo relacionamento**
    pagamento = db.relationship("Pagamento", back_populates="pedido", uselist=False)

    # opcional: armazena o valor final (setado ao finalizar)
    valor_total = db.Column(db.Float, nullable=True)

    def __repr__(self):
        nome = self.cliente.nome if self.cliente else "—"
        return f"<Pedido {self.id} - Cliente {nome} - Status: {self.status}>"