# app/models/cliente.py
from app.models.database import db

class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(30), nullable=True)
    placa_veiculo = db.Column(db.String(20), nullable=True) # no lugar da classe veiculo

    # Novo campo CPF (único e obrigatório)
    cpf = db.Column(db.String(14), unique=True, nullable=True)  
    # formato esperado: 000.000.000-00 (ou sem máscara, você decide depois)

    # Relacionamentos existentes
    reservas = db.relationship("ReservaMesa", back_populates="cliente", lazy=True)
    
    # Relacionamento que vamos usar ao criar pedidos (deixa preparado)
    pedidos = db.relationship("Pedido", back_populates="cliente", lazy=True)

    def __repr__(self):
        return f"<Cliente {self.id} - {self.nome} ({self.cpf})>"
