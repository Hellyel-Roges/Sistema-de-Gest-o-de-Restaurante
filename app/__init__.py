from flask import Flask
from app.models.database import db

def create_app():
    app = Flask(__name__)

    # Configurações do banco
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o banco
    db.init_app(app)

    # Importa todos os modelos para criar as tabelas
    from app.models.cliente import Cliente
    from app.models.veiculo import Veiculo
    from app.models.mesa import Mesa
    from app.models.reserva_mesa import ReservaMesa

    with app.app_context():
        db.create_all()  # Cria todas as tabelas

        # Criar mesas se não existirem
        if not Mesa.query.first():
            for i in range(1, 11):  # 10 mesas
                db.session.add(Mesa(numero=i))
            db.session.commit()

    # Importa blueprints
    from app.routes.paginas_routes import paginas_bp
    from app.routes.reserva_api import reservas_api

    # Registra blueprints
    app.register_blueprint(paginas_bp)
    app.register_blueprint(reservas_api, url_prefix="/api")  # exemplo: prefixo /api

    return app
