"""Utility decorators for view functions."""

from functools import wraps

from flask import flash, redirect, session, url_for


def login_required(f):
    """Redirect to login if the member is not authenticated."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "member_id" not in session:
            flash(
                "Devi effettuare l'accesso per visualizzare questa pagina.",
                "warning",
            )
            return redirect(url_for("member.login"))
        return f(*args, **kwargs)

    return decorated_function
