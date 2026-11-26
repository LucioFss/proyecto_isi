from datetime import UTC, datetime

from proyecto_isi.extensions import db


class AnswerVote(db.Model):
    __tablename__ = "answer_votes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("User.id"), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey("answer.id_answer"), nullable=False)
    value = db.Column(db.Integer, nullable=False)  # 1 o -1

    __table_args__ = (
        db.UniqueConstraint("user_id", "answer_id", name="uq_user_answer_vote"),
    )


class Answer(db.Model):
    __tablename__ = 'answer'

    id_answer = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    author_id = db.Column(db.String(36), db.ForeignKey("User.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    author = db.relationship("User", backref="answers")
    question = db.relationship("Question", back_populates="answers")

    votes = db.relationship("AnswerVote", backref="answer", lazy="dynamic", cascade="all, delete-orphan")

    def registrar_voto(self, user_id: str, value: int):
        if value not in (1, -1):
            raise ValueError("El voto debe ser 1 (positivo) o -1 (negativo)")

        voto_existente = self.votes.filter_by(user_id=user_id).first()

        if voto_existente:
            if voto_existente.value == value:
                db.session.delete(voto_existente)
            else:
                voto_existente.value = value
        else:
            nuevo_voto = AnswerVote(user_id=user_id, answer_id=self.id_answer, value=value)
            db.session.add(nuevo_voto)

    @property
    def votos_positivos(self) -> int:
        return self.votes.filter_by(value=1).count()

    @property
    def votos_negativos(self) -> int:
        return self.votes.filter_by(value=-1).count()
