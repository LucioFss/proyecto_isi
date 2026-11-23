from datetime import timezone
from datetime import datetime, UTC
from proyecto_isi.extensions import db
from sqlalchemy.sql import Nullable

class Answer(db.Model):
    __tablename__ = 'answer'
    id_answer = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String, Nullable = False)
    publication_date = db.Column(db.DateTime, Nullable = False, default = lambda : datetime.now(UTC))
