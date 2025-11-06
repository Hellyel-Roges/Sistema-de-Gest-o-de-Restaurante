# app/models/veiculo.py
from app.models.database import db

class Veiculo(db.Model):
    __tablename__ = "veiculos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    placa = db.Column(db.String(10), nullable=False)

    # FK para cliente
    dono_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    dono = db.relationship("Cliente", back_populates="veiculos")

    def __repr__(self):
        return f"<Veículo {self.placa}>"
