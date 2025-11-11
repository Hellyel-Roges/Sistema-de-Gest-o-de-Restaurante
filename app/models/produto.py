# app/models/produto.py
from app.models.database import db

class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(120), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(250), nullable=False)

    # ligação com pedidos (via tabela intermediária)
    itens_pedido = db.relationship("PedidoProduto", back_populates="produto")

    def __repr__(self):
        return f"<Produto {self.nome} - R${self.preco:.2f}>"
