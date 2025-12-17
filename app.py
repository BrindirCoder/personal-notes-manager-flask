from flask import Flask,flash,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_wtf.csrf import  CSRFError


csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///personal_notes.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "super-secret-key-change-this"

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.data import register_data
    register_data(app)

    from routes.auth import register_auth
    register_auth(app)

    # NEW CSRF ERROR HANDLER
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        flash("CSRF token missing or invalid. Please try again.", "error")
        # redirect back to previous page or login
        return redirect(request.referrer or url_for("login"))

    return app
