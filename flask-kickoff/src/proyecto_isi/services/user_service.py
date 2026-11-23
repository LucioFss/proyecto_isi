from werkzeug.security import check_password_hash,generate_password_hash
from proyecto_isi.extensions import db
from proyecto_isi.models.User import User
#ARCHIVO QUE IMPLEMENTA TODA LA LOGICA DE GESTION DE Usuario
def register_user(name : str, password : str):
    #Se usa scalar_one_or_none() en vez de scalar_one, por que el primero se usa cuando no sabes si
    # el registro existe, devolviendo none si no existe
    # El segundo sevuelve una exepcion si no lo encuentra, lo que romperia la logica
    #Esta es una consulta ejecutada mediante flask-sqlalchemy
    search_user = db.session.execute(db.select(User).filter_by(name=name)).scalar_one_or_none()

    if(search_user is not None):
        raise ValueError("El nombre de el usuario ya esta en uso")

    #Encriptamos la contraseña
    new_password_hash = generate_password_hash(password)
    new_user = User()
    new_user.name = name
    new_user.password_hash = new_password_hash

    db.session.add(new_user)
    db.session.commit()

def check_password(password_hash : str, plain_password : str):
    #Metodo de werkzeug.security que compara un hash con un texto plano y verifica si son iguales,
    # true si son iguales, false si no lo son
    return check_password_hash(password_hash, plain_password)

#Metodo que compara una contraseña en hash con una en texto plano, para verificar si es la misma contraseña
def authenticate_user(name : str, password : str):

    search_user = db.session.execute(db.select(User).filter_by(name=name)).scalar_one_or_none()
    if(search_user is None or not check_password(search_user.password_hash, password)):
        #Si el usuario no existe o la contraseña es incorrecta entonces lanzamos una exepcion
        raise ValueError("Usuario o contraseña incorrectos")

    #Si el usuario es correcto y la contraseña tambien, entonces se incia sesion
    return search_user

def get_user_by_id(user_id : str):
    search_user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
    #No devolvemos una exepcion por que el resultado es un None o el usuario, son resultados posibles de la busqueda,
    # y no un error,ademas flask-login exige que se devuelva None o el usuario
    return search_user
