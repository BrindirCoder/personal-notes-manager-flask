from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Note
from app import db


def register_data(app):

    @login_required
    @app.route("/show_data")
    def show_data():
        category = request.args.get("category", "All")
        search_query = request.args.get("q", "").strip()

        query = Note.query.filter_by(user_id=current_user.id)

        if category != "All":
            query = query.filter(Note.category == category)

        if search_query:
            query = query.filter(Note.title.ilike(f"%{search_query}%"))

        notes = query.all()

        return render_template(
            "index.html",
            notes=notes,
            selected_category=category,
            search_query=search_query,
        )

    @app.route("/add_note", methods=["GET", "POST"])
    @login_required
    def add_note():
        if request.method == "POST":
            new_note = Note(
                title=request.form.get("title"),
                content=request.form.get("content"),
                category=request.form.get("category"),
                user_id=current_user.id,
            )
            db.session.add(new_note)
            db.session.commit()

            flash("Your note was added successfully", "success")
            return redirect(url_for("show_data"))

        return render_template("add_note.html")

    @app.route("/edit_note/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_note(id):
        note = Note.query.get_or_404(id)

        if request.method == "POST":
            note.title = request.form.get("title")
            note.content = request.form.get("content")
            note.category = request.form.get("category")

            db.session.commit()
            flash("Note updated successfully", "info")
            return redirect(url_for("show_data"))

        return render_template("edit_note.html", note=note)

    @app.route("/delete_note/<int:id>", methods=["POST"])
    @login_required
    def delete_note(id):
        note = Note.query.get_or_404(id)
        db.session.delete(note)
        db.session.commit()

        flash("Note deleted successfully", "delete")
        return redirect(url_for("show_data"))
