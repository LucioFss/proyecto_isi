#Modulo que conecta el programa con el sistema operativo
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

#Inicializamos una variable que inizaliza el contructor de una base de datos mediante SQLalchemy
db = SQLAlchemy()

#Inicializamos el objeto login_manager para la logica de incio de sesion y registro
login_manager = LoginManager()
#Configuramos a donde redirigir a un usuario anonimo si intenta entrar a una ruta protegida con @login_required
login_manager.login_view = "users.login" # type: ignore
