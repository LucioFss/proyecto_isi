
from datetime import datetime, timezone, UTC
from flask import Flask, render_template, request, redirect, url_for
from proyecto_isi.config import Config
from proyecto_isi.extensions import db
from proyecto_isi.models.Question import Question

#Clase que crea y configura una aplicacion web con flask
def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)


    #from proyecto_isi.api.health import health_bp
    #from proyecto_isi.web.users import users_bp

    #app.register_blueprint(health_bp)
    #app.register_blueprint(users_bp)
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
