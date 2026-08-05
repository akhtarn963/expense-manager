from flask import Flask

from app.extensions import db, migrate
from app.utils import format_money
from app.helpers import load_logged_in_user


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    app.jinja_env.globals["format_money"] = format_money

    from app.routes import dashboard_bp, expense_bp, auth_bp, category_bp, profile_bp
    
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(profile_bp)

    @app.before_request
    def before_request():
        load_logged_in_user()

    return app