from datetime import datetime, UTC
from proyecto_isi.extensions import db

class QuestionVote(db.Model):
    __tablename__ = "question_votes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("User.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    # 1 para positivo, -1 para negativo
    value = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "question_id", name="uq_user_question_vote"),
    )


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.String(36), db.ForeignKey("User.id"), nullable=True)
    author = db.relationship("User")
    title = db.Column(db.String, nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    
    # Relación con los votos (cascade borra los votos si se borra la pregunta)
    votes = db.relationship("QuestionVote", backref="question", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, title: str, publication_date: datetime | None = None):
        self.title = title
        self.publication_date = publication_date or datetime.now(UTC)

    def registrar_voto(self, user_id: str, value: int):
        """Registra un voto (1 o -1). Si ya existe, lo actualiza o lo quita si repite."""
        if value not in (1, -1):
            raise ValueError("El voto debe ser 1 (positivo) o -1 (negativo)")

        voto_existente = self.votes.filter_by(user_id=user_id).first()

        if voto_existente:
            if voto_existente.value == value:
                # Si hace clic de nuevo en el mismo voto, lo quita (toggle)
                db.session.delete(voto_existente)
            else:
                # Si cambia de positivo a negativo (o viceversa), lo actualiza
                voto_existente.value = value
        else:
            nuevo_voto = QuestionVote(user_id=user_id, question_id=self.id, value=value)
            db.session.add(nuevo_voto)

    @property
    def votos_positivos(self) -> int:
        return self.votes.filter_by(value=1).count()

    @property
    def votos_negativos(self) -> int:
        return self.votes.filter_by(value=-1).count()
