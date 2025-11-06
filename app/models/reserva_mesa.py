# app/models/reserva_mesa.py
from app.models.database import db
from datetime import datetime

class ReservaMesa(db.Model):
    __tablename__ = "reservas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_mesa = db.Column(db.Integer, nullable=False)
    horario_de_entrada = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    horario_de_saida = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # FK para cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    cliente = db.relationship("Cliente", back_populates="reservas")

    # FK para mesa
    mesa_id = db.Column(db.Integer, db.ForeignKey("mesas.id"), nullable=True)
    mesa = db.relationship("Mesa", back_populates="reservas")

    def __repr__(self):
        nome = self.cliente.nome if self.cliente else "—"
        return f"<Reserva Mesa {self.numero_mesa} - Cliente {nome}>"
