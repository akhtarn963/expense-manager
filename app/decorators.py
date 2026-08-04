from functools import wraps
from flask import session, redirect, url_for, flash,g


def login_required(view):

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if g.user is None:
            flash("Please login first.", "warning")
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view