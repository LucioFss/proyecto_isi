from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login.utils import login_required, login_user, logout_user

from proyecto_isi.services.user_service import authenticate_user, register_user

users_bp = Blueprint("users", __name__)

#Metodo que se encarga de tratar el registro de un usuario en el sistema
# lo redirige a la pantalla de inicio de sesion en el caso de exito
@users_bp.route("/register", methods = ["GET", "POST"])
def register():
    if (request.method == 'POST'):
        #Se ingresa el nombre, si el parametro es none, se reemplaza con la la cadena vacia
        # strip() quita los espacios innecesarios entre palabras
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")
        try:
            register_user(name, password)
            #Enviamos un mensaje corto desde el codigo a la plantilla
            flash("usuario registrado correctamente. Ya puedes iniciar sesion.")
            return redirect(url_for("users.login"))
        except Exception as e:
            #Se imprime la exepcion en pantalla
            flash(str(e))
    #Peticion GET sin comprobacion
    return render_template("register.html")

#Metodo que se encarga de tratar el inicio de sesion de un usuario
# en el caso de exito lo redirige a la pantalla de inicio
@users_bp.route("/login", methods=["GET","POST"])
def login():
    if(request.method=="POST"):
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")
        try:
            #Verificamos si el usuario existe
            user = authenticate_user(name, password)
            #Si el usuario existe
            login_user(user)
            return redirect(url_for("inicio"))
        except Exception as e:
            flash(str(e))

    return render_template("login.html")

#Metodo que se encarga de gestionar el cierre de sesion de un usuario
@users_bp.route("/logout")
@login_required
def logout():
    #Se cierra la sesion de el usuario actual
    logout_user()
    #Se redirecciona al usuario a la pantalla de inicio de sesion
    return redirect(url_for("users.login"))
