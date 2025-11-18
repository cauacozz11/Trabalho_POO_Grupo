# __init__.py (Atualizado)
from flask import Flask
from database import db, Cliente, Material, Emprestimo # Importamos o db e os Modelos

def create_app():
    app = Flask(__name__)

    # --- Configurações ---
    # Chave Secreta para Flash Messages
    app.config['SECRET_KEY'] = 'chave_secreta_para_biblioteca' 
    # URI do Banco de Dados SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca_completa.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    # 1. Inicializa o Flask-SQLAlchemy (vincula o 'db' ao app Flask)
    db.init_app(app)

    # 2. Importa e Registra o Blueprint
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # 3. Cria as tabelas do banco de dados (se não existirem)
    with app.app_context():
        db.create_all() 

    return app