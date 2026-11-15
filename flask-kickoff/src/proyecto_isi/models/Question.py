from proyecto_isi.extensions import db

class Question(db.Model):
    #Declaramos el nombre de la tabla
    __tablename__ = "questions"

    #Declaracion de los atributos y sus restricciones

    #Declaramos el atributo id como un entero y que sea la clave primaria de la tabla
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    publication_date = db.Column(db.DateTime, nullable = False)
