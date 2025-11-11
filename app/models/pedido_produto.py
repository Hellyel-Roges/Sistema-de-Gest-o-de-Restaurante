# app/models/pedido_produto.py
from app.models.database import db

class PedidoProduto(db.Model):
    __tablename__ = "pedido_produto"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)

    quantidade = db.Column(db.Integer, nullable=False, default=1)

    pedido = db.relationship("Pedido", back_populates="itens")
    produto = db.relationship("Produto", back_populates="itens_pedido")

    def __repr__(self):
        return f"<PedidoProduto Pedido={self.pedido_id} Produto={self.produto_id} Qtd={self.quantidade}>"
