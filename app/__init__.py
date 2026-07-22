from flask import Flask

from app.extensions import db, migrate
from app.utils import format_money


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    app.jinja_env.globals["format_money"] = format_money

    from app.routes import expense_bp
    app.register_blueprint(expense_bp)

    return app