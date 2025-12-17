from flask import request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
import re
from datetime import datetime, timedelta
from models import User
from app import db


def register_auth(app):
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email_or_username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter(
                (User.username == email_or_username) | (User.email == email_or_username)
            ).first()

            # Check account lock
            if user and user.lock_until and datetime.utcnow() < user.lock_until:
                remaining = int((user.lock_until - datetime.utcnow()).total_seconds() / 60) + 1
                flash(f"Too many failed attempts. Try again in {remaining} minute(s).", "error")
                return redirect(url_for("login"))

            # Correct password
            if user and check_password_hash(user.password, password):
                user.failed_login_attempts = 0
                user.lock_until = None
                db.session.commit()
                login_user(user)
                flash("Logged in successfully!", "success")
                return redirect(url_for("show_data"))

            # Wrong password
            if user:
                user.failed_login_attempts = user.failed_login_attempts or 0
                user.failed_login_attempts += 1

                if user.failed_login_attempts >= 3:
                    user.lock_until = datetime.utcnow() + timedelta(minutes=30)
                    flash("Account locked for 30 minutes due to multiple failed login attempts.", "error")
                else:
                    remaining = 3 - user.failed_login_attempts
                    flash(f"Invalid credentials. {remaining} attempt(s) left.", "error")
                db.session.commit()
            else:
                flash("Invalid username/email or password.", "error")

            return redirect(url_for("login"))

        return render_template("login.html")

    @app.route("/")
    def home():
        return redirect(url_for("login"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm = request.form.get("confirm")

            if password != confirm:
                flash("Passwords do not match", "error")
                return redirect(url_for("register"))

            if User.query.filter_by(username=username).first():
                flash("Username already exists", "error")
                return redirect(url_for("register"))

            if User.query.filter_by(email=email).first():
                flash("Email already registered", "error")
                return redirect(url_for("register"))

            # Password strength check
            def is_strong_password(password):
                return (
                    len(password) >= 8 and
                    re.search(r"[A-Z]", password) and
                    re.search(r"[a-z]", password) and
                    re.search(r"[0-9]", password) and
                    re.search(r"[@#$%!^&*()_+=\-{}[\]:;\"'<>,.?/]", password)
                )

            if not is_strong_password(password):
                flash(
                    "Password must be at least 8 characters and include uppercase, lowercase, number, and special character (@#$%)",
                    "error",
                )
                return redirect(url_for("register"))

            new_user = User(username=username, email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out successfully", "success")
        return redirect(url_for("login"))
