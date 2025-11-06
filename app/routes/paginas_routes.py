from flask import Blueprint, render_template

paginas_bp = Blueprint("paginas", __name__)

@paginas_bp.route("/")
def home():
    return render_template("index.html", title="La Forchetta 🍝")

@paginas_bp.route("/reserva_mesa")
def reserva_mesa_page():
    return render_template("reserva_mesa.html", title="Reservas - La Forchetta")