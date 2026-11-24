from flask import Blueprint, abort, redirect, request, url_for
from flask_login import current_user, login_required
from proyecto_isi.extensions import db
from proyecto_isi.models.Answers import Answer
from proyecto_isi.models.Question import Question

answers_bp = Blueprint("answers", __name__)


@answers_bp.route("/question/<int:question_id>/answer", methods=["POST"])
@login_required
def create_answer(question_id: int):
    question = db.session.get(Question, question_id)
    if question is None:
        abort(404)

    body = request.form.get("body", "").strip()
    if not body:
        return "La respuesta no puede estar vacía", 400

    answer = Answer(
        body=body,
        author=current_user._get_current_object(),
        question=question,
    )
    db.session.add(answer)
    db.session.commit()

    return redirect(url_for("questions.all_questions", _anchor=f"question-{question.id}"))
