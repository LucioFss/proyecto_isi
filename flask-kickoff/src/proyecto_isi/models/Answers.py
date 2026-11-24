from datetime import datetime, UTC
from proyecto_isi.extensions import db

class Answer(db.Model):
    __tablename__ = 'answer'
    id_answer = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String, nullable = False)
    publication_date = db.Column(db.DateTime, nullable = False, default = lambda : datetime.now(UTC))
    author_id = db.Column(db.String(36), db.ForeignKey("User.id"), nullable = False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable = False)
    author = db.relationship("User", backref="answers")
    question = db.relationship("Question", backref="answers")
