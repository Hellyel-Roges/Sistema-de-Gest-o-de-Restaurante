# app/__init__.py
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
    from app.models.mesa import Mesa
    from app.models.reserva_mesa import ReservaMesa
    from app.models.pagamento import Pagamento
    from app.models.produto import Produto
    from app.models.pedido import Pedido
    from app.models.pedido_produto import PedidoProduto

    with app.app_context():
        db.create_all()  # Cria todas as tabelas

        # Criar mesas se não existirem
        if not Mesa.query.first():
            for i in range(1, 11):  # 10 mesas
                db.session.add(Mesa(numero=i))
            db.session.commit()

        # Criar produtos padrão se não existirem
        if not Produto.query.first():
            produtos_iniciais = [
                Produto(nome="Lasanha", descricao="Lasanha artesanal com molho especial.", preco=35.00),
                Produto(nome="Espaguete", descricao="Espaguete ao molho de tomate fresco.", preco=30.00),
                Produto(nome="Ravioli", descricao="Ravioli recheado com ricota e espinafre.", preco=32.00),
                Produto(nome="Gnocchi", descricao="Nhoque caseiro ao molho bolonhesa.", preco=33.00),
                Produto(nome="Fettuccine Alfredo", descricao="Fettuccine cremoso com parmesão.", preco=34.00),
            ]
            db.session.add_all(produtos_iniciais)
            db.session.commit()

    # Importa blueprints
    from app.routes.paginas_routes import paginas_bp
    from app.routes.reserva_api import reservas_api
    from app.routes.pedido_api import pedido_api
    from app.routes.produto_api import produto_api


    # Registra blueprints
    app.register_blueprint(paginas_bp)
    app.register_blueprint(reservas_api, url_prefix="/api")  # exemplo: prefixo /api
    app.register_blueprint(pedido_api, url_prefix="/api")
    app.register_blueprint(produto_api, url_prefix="/api")

    return app
