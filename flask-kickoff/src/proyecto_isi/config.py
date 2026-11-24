import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "dataBase.db"

class Config:
    #Sello de seguridad proporcionado por el sistema operativo para la conexion con la base de datos
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-key")
    #Conexion con la base de datos SQLITE "dataBase"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{DB_PATH}",
    )
