from datetime import UTC, datetime

from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from proyecto_isi.extensions import db
from proyecto_isi.models.Question import Question

questions_bp = Blueprint("questions", __name__)

@questions_bp.route("/question/create", methods=["GET", "POST"])
def create_question():
    if request.method == "POST":
        new_title = request.form.get("title")
        if not new_title:
            return "El título es obligatorio", 400
        new_question = Question(
            title = new_title,
            publication_date=datetime.now(UTC)
        )
        if current_user.is_authenticated:
            new_question.author_id = current_user.get_id()

        try:
            db.session.add(new_question)
            db.session.commit()
            # Redirige a la página principal tras guardar
        except Exception as e:
            db.session.rollback()
            return f"Error al guardar: {e}", 500

        return redirect(url_for("questions.create_question"))
    # Con simplemente el GET, mostramos el formulario y las existentes.
    preguntas = Question.query.order_by(Question.publication_date.desc()).all() 
    return render_template("create_question.html", preguntas=preguntas)

@questions_bp.route("/question")
def all_questions():
    preguntas = Question.query.order_by(Question.publication_date.desc()).all()  
    return render_template("all_questions.html", preguntas=preguntas)

@questions_bp.route("/question/<int:question_id>/delete", methods=["POST"])
@login_required
def delete_question(question_id: int):
    if not current_user.is_admin:
        abort(403)

    question = db.session.get(Question, question_id)
    if question is None:
        abort(404)

    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("questions.all_questions"))

@questions_bp.route("/question/<int:question_id>/vote", methods=["POST"])
@login_required
def vote_question(question_id: int):
    question = db.session.get(Question, question_id)
    if question is None:
        abort(404)
    try:
        value = int(request.form.get("value", 0))
        question.registrar_voto(user_id=current_user.get_id(), value=value)
        db.session.commit()
    except ValueError:
        return "Valor de voto inválido", 400
    except Exception as e:
        db.session.rollback()
        return f"Error al registrar el voto: {e}", 500

    return redirect(url_for("questions.all_questions", _anchor=f"question-{question.id}"))