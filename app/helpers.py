from flask import g, session

from app.models import User


def load_logged_in_user():
    """
    Load the currently logged-in user into flask.g
    """

    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()