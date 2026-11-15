#Modulo que conecta el programa con el sistema operativo
import os
import flask
from flask_sqlalchemy import SQLAlchemy

#Inicializamos una variable que inizaliza el contructor de una base de datos mediante SQLalchemy
db = SQLAlchemy()
