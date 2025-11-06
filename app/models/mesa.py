# app/models/mesa.py
from app.models.database import db

class Mesa(db.Model):
    __tablename__ = "mesas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)

    # Relacionamento com reservas
    reservas = db.relationship("ReservaMesa", back_populates="mesa", lazy=True)

    def __repr__(self):
        return f"<Mesa {self.numero}>"
