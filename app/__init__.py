from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Faça login para acessar esta página.'
login_manager.login_message_category = 'warning'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.alunos import alunos_bp
    from app.routes.instrutores import instrutores_bp
    from app.routes.veiculos import veiculos_bp
    from app.routes.agendamentos import agendamentos_bp
    from app.routes.presenca import presenca_bp
    from app.routes.pagamentos import pagamentos_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(alunos_bp)
    app.register_blueprint(instrutores_bp)
    app.register_blueprint(veiculos_bp)
    app.register_blueprint(agendamentos_bp)
    app.register_blueprint(presenca_bp)
    app.register_blueprint(pagamentos_bp)

    with app.app_context():
        db.create_all()
        _seed_admin()

    return app


def _seed_admin():
    from app.models import Usuario
    if not Usuario.query.filter_by(email='admin@ecodrive.com').first():
        admin = Usuario(nome='Administrador', email='admin@ecodrive.com',
                        cpf='00000000000', perfil='admin')
        admin.set_senha('admin123')
        db.session.add(admin)
        db.session.commit()
