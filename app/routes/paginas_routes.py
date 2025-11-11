# app/routes/paginas_routes.py
from flask import Blueprint, render_template
from app.models.produto import Produto

paginas_bp = Blueprint("paginas", __name__)

@paginas_bp.route("/")
def home():
    return render_template("index.html", title="La Forchetta 🍝")

@paginas_bp.route("/reserva_mesa")
def reserva_mesa_page():
    return render_template("reserva_mesa.html", title="Reservas - La Forchetta")

@paginas_bp.route("/delivery")
def delivery_page():
    produtos = Produto.query.all()
    return render_template("delivery.html", title="Delivery - La Forchetta", produtos=produtos)