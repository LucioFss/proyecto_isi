from flask import Blueprint,request,render_template,redirect,url_for
from datetime import datetime, timezone, UTC
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
        try:
            db.session.add(new_question)
            db.session.commit()
            # Redirige a la página principal tras guardar
        except Exception as e:
            db.session.rollback()
            return f"Error al guardar: {e}", 500

        return redirect(url_for("questions.create_question"))
    # Con simplemente el GET, mostramos el formulario y las existentes.
    preguntas = Question.query.order_by(Question.publication_date.desc()).all()  # pyright: ignore[reportAttributeAccessIssue]
    return render_template("create_question.html", preguntas=preguntas)

@questions_bp.route("/question")
def all_questions():
    preguntas = Question.query.order_by(Question.publication_date.desc()).all()  # pyright: ignore[reportAttributeAccessIssue]
    return render_template("all_questions.html", preguntas=preguntas)
