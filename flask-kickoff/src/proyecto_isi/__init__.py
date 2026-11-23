
from datetime import datetime, timezone, UTC
from flask import Flask, render_template, request, redirect, url_for
from proyecto_isi.config import Config
from proyecto_isi.extensions import db, login_manager

from proyecto_isi.services.user_service import get_user_by_id

from proyecto_isi.models.Question import Question

#Clase que crea y configura una aplicacion web con flask
def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    # Se inicializa la conexion con la base de datos
    db.init_app(app)

    # Se inicializa la conexion con el login manager
    login_manager.init_app(app)
    # Se importa el blueprint de health check
    from proyecto_isi.api.health import health_bp

    # Se importa el blueprint de users, que es donde esta toda la gestion de rutas de usuario
    from proyecto_isi.web.users import users_bp

    # Carga el usuario autenticado desde la BD usando el ID de la cookie de sesión
    @login_manager.user_loader
    def load_user(user_id: str):
        return get_user_by_id(user_id)

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(users_bp)

    @app.route("/")
    def inicio():
        return "servidor funcionando..."

    @app.route("/preguntas/crear", methods=["GET", "POST"])
    def crear_pregunta():
        if request.method == "POST":
            titulo = request.form.get("title")
            if not titulo:
                return "El título es obligatorio", 400
            nueva_pregunta = Question(
                title =titulo,
                publication_date=datetime.now(UTC)
            )
            try:
                db.session.add(nueva_pregunta)
                db.session.commit()
                # Redirige a la página principal tras guardar
                return redirect(url_for("crear_pregunta"))
            except Exception as e:
                db.session.rollback()
                return f"Error al guardar: {e}", 500
        # Con simplemente el GET, mostramos el formulario y las existentes.
        preguntas = Question.query.order_by(Question.publication_date.desc()).all()
        return render_template("crear_pregunta.html", preguntas=preguntas)

    return app
