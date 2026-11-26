import uuid

from flask_login import UserMixin
from sqlalchemy import false

from proyecto_isi.extensions import db


class User(UserMixin,db.Model):
    __tablename__ = "User"

    #Id de usuario autogenerado con uuid
    id = db.Column(db.String(36), primary_key = True, default = lambda : str(uuid.uuid4()))
    name = db.Column(db.String(20), nullable = False, unique = True)
    #Se declara el campo de la contraseña de el usuario
    # Es un campo que guarda un hash muy muy largo de tipo String
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, nullable=False, default=False, server_default=false())
