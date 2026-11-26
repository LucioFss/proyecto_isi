from flask import Flask, redirect, render_template, request, url_for

from proyecto_isi.config import Config
from proyecto_isi.extensions import db, login_manager
from proyecto_isi.models.Answers import Answer
from proyecto_isi.models.Question import Question
from proyecto_isi.services.user_service import get_user_by_id


#Clase que crea y configura una aplicacion web con flask
def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    # Se inicializa la conexion con la base de datos
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Crea las tablas de la base de datos si no existen

    # Se inicializa la conexion con el login manager
    login_manager.init_app(app)

    # Se importa el blueprint de health check
    from proyecto_isi.api.health import health_bp
    from proyecto_isi.web.answers import answers_bp
    from proyecto_isi.web.questions import questions_bp

    # Se importa el blueprint de users, que es donde esta toda la gestion de rutas de usuario
    from proyecto_isi.web.users import users_bp

    # Carga el usuario autenticado desde la BD usando el ID de la cookie de sesión
    @login_manager.user_loader
    def load_user(user_id: str):
        return get_user_by_id(user_id)

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(users_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(answers_bp)

    @app.route("/")
    def inicio():
        return render_template("home_page.html")


    return app
