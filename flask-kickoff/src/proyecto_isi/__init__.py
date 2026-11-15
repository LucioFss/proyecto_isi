from flask import Flask


from proyecto_isi.config import Config
from proyecto_isi.extensions import db

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

    return app
