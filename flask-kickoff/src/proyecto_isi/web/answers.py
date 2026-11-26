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

@answers_bp.route("/answer/<int:answer_id>/delete", methods=["POST"])
@login_required
def delete_answer(answer_id: int):
    if not current_user.is_admin:
        abort(403)

    answer = db.session.get(Answer, answer_id)
    if answer is None:
        abort(404)

    question_id = answer.question_id
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for("questions.all_questions", _anchor=f"question-{question_id}"))

@answers_bp.route("/answer/<int:answer_id>/vote", methods=["POST"])
@login_required
def vote_answer(answer_id: int):
    answer = db.session.get(Answer, answer_id)
    if answer is None:
        abort(404)

    try:
        value = int(request.form.get("value", 0))
        answer.registrar_voto(user_id=current_user.get_id(), value=value)
        db.session.commit()
    except ValueError:
        return "Valor de voto inválido", 400
    except Exception as e:
        db.session.rollback()
        return f"Error al registrar el voto: {e}", 500

    return redirect(url_for("questions.all_questions", _anchor=f"question-{answer.question_id}"))
