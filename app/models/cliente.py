# app/models/cliente.py
from app.models.database import db

class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(30), nullable=True)

    # Relacionamentos
    reservas = db.relationship("ReservaMesa", back_populates="cliente", lazy=True)
    veiculos = db.relationship("Veiculo", back_populates="dono", lazy=True)

    def __repr__(self):
        return f"<Cliente {self.id} - {self.nome}>"
